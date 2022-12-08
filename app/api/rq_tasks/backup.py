from django_rq import job
import django_rq
from api.models import Backup, BackupJob, BackupJobSecret, BackupJobStorageModule, Secret, BackupExecution, Parameter, \
    StorageExecution, System
import time
from django.utils.timezone import now

from api.utils.backup_job_util import BackupJobUtil
from api.utils.package_util import PackageUtil
from api.serializers import SecretGbModuleSerializer, ParameterGbModuleSerializer, SystemGbModuleSerializer

@job
def backup(backup_job: BackupJob, backup_module, storage_modules: [BackupJobStorageModule], user):
    # start a backup_execution
    backup_execution = BackupExecution.objects.create(created_by=user, backup_job=backup_job, backup_module=backup_module)
    package_instance = None
    do_backup_response = None
    system_dict = SystemGbModuleSerializer(backup_job.system).data
    # get an instance of the plugin
    try:
        package_instance = PackageUtil.get_python_class_of_module(backup_module)()
    except FileNotFoundError as e:
        print("file not found error at loading backup_instance")
        backup_execution.errors = f"file not found error: {e}"
    except Exception as e:
        print("error at loading backup_instance")
        backup_execution.errors = f"file not found error: {e}"

    if not package_instance:
        backup_execution.save()
        return

    if package_instance:
        # inject the secrets
        package_instance.secrets = BackupJobUtil.parsed_secret_array(backup_job)

        # inject the params
        backup_parameters = Parameter.objects.filter(backup_job_parameter_parameter__backup_job=backup_job).distinct()
        package_instance.parameters = [dict(d) for d in ParameterGbModuleSerializer(backup_parameters, many=True).data]

        # inject the system
        package_instance.system = system_dict

        # inject the log function
        def backup_log(message):
            message = f"{now()} - {message}\n"
            print(message)
            if not backup_execution.logs:
                backup_execution.logs = message
            else:
                backup_execution.logs += message
            backup_execution.save()
        package_instance.log = backup_log
        backup_log(f"secrets: {package_instance.secrets}")
        backup_log(f"params: {package_instance.parameters}")
        # do backup and fetch response (which is a backup_result type)
        try:
            do_backup_response = package_instance.do_backup()
        except Exception as error:
            print(f"error: ", error)
            backup_execution.state = 2
            backup_execution.errors = error

    # end the backup_execution
    backup_execution.ends_at = now()
    backup_execution.state = 3
    if not do_backup_response or do_backup_response.error:
        backup_execution.state = 2
        if do_backup_response:
            backup_execution.errors = (backup_execution.errors or "") + (do_backup_response.error or "")
        elif not backup_execution.errors:
            backup_execution.errors = "UNKNOWN ERROR"
    if do_backup_response:
        backup_execution.output = do_backup_response.output
    backup_execution.save()

    # return if we had an error
    if backup_execution.state == 2:
        return

    # in loop create a module_instance, inject secrets and params, create a storage_execution,
    # create the backup and save it with the store_module, create the backup object, and end the storage_execution
    for storage_module_pivot in storage_modules:
        storage_module = storage_module_pivot.storage_module
        # start a storage_execution
        storage_execution = StorageExecution.objects.create(created_by=user, backup_job=backup_job, storage_module=storage_module)
        storage_package_instance = None
        do_storage_response = None
        try:
            storage_package_instance = PackageUtil.get_python_class_of_module(storage_module)()
        except FileNotFoundError as e:
            print("file not found error at loading backup_instance")
            storage_execution.errors = f"file not found error: {e}"
        except Exception as e:
            print("error at loading backup_instance")
            storage_execution.errors = f"file not found error: {e}"

        if storage_package_instance:
            # inject the secrets
            storage_secrets = Secret.objects.filter(
                backup_job_storage_model_secret_secret__backup_job_storage_module=storage_module_pivot
            ).distinct()
            storage_package_instance.secrets = [dict(d) for d in SecretGbModuleSerializer(storage_secrets, many=True).data]

            # inject the params
            storage_parameters = Parameter.objects.filter(
                backup_job_storage_model_parameter_parameter__backup_job_storage_module=storage_module_pivot
            ).distinct()
            storage_package_instance.parameters = [dict(d) for d in ParameterGbModuleSerializer(storage_parameters, many=True).data]

            # inject the system
            storage_package_instance.system = system_dict

            # inject encryption_secret if specified
            if storage_module_pivot.encryption_secret:
                storage_package_instance.encryption_secret = SecretGbModuleSerializer(
                    storage_module_pivot.encryption_secret).data

            # inject the log function
            def storage_log(message):
                message = f"{now()} - {message}\n"
                print(message)
                if not storage_execution.logs:
                    storage_execution.logs = message
                else:
                    storage_execution.logs += message
                storage_execution.save()
            storage_package_instance.log = storage_log

            # do storage and fetch response (which is a storage_result type)
            try:
                do_storage_response = storage_package_instance.save_to_storage(do_backup_response)
            except Exception as error:
                print(f"error: ", error)
                storage_execution.state = 2
                storage_execution.errors = error
    
        # end the storage_execution
        storage_execution.ends_at = now()
        storage_execution.state = 3
        if not do_storage_response or do_storage_response.error:
            storage_execution.state = 2
            if do_storage_response:
                storage_execution.errors = (storage_execution.errors or "") + (do_storage_response.error or "")
            elif not storage_execution.errors:
                storage_execution.errors = "UNKNOWN ERROR"
        if do_storage_response:
            storage_execution.output = do_storage_response.output

        storage_execution.save()

        # return if we had an error
        if storage_execution.state == 2:
            return

        # save backup
        backup = Backup.objects.create(
            name=backup_job.name,
            created_by=user,
            path=do_storage_response.path,
            backup_job=backup_job,
            backup_module=backup_module,
            storage_module=storage_module,
            additional_parameters=do_storage_response.additional_parameters_dict,
            backup_execution=backup_execution,
            storage_execution=storage_execution
        )
