from django_rq import job
import django_rq
from api.models import Backup, BackupJob, BackupJobSecret, BackupJobStorageModule, Secret, BackupExecution, Parameter
import time
from django.utils.timezone import now

from api.utils.package_util import PackageUtil
from api.serializers import SecretGbModuleSerializer, ParameterGbModuleSerializer

@job
def backup(backup_job: BackupJob, backup_module, storageModules: [BackupJobStorageModule], user):
    # get an instance of the plugin
    package_instance = PackageUtil.get_python_class_of_module(backup_module)()

    # inject the secrets
    backup_secrets = Secret.objects.filter(backup_job_secret_secret__backup_job=backup_job).distinct()
    package_instance.secrets = SecretGbModuleSerializer(backup_secrets, many=True).data

    # inject the params
    backup_parameters = Parameter.objects.filter(backup_job_parameter_parameter__backup_job=backup_job).distinct()
    package_instance.parameters = ParameterGbModuleSerializer(backup_parameters, many=True).data

    # start a backup_execution
    backup_execution = BackupExecution.objects.create(created_by=user, backup_job=backup_job, backup_module=backup_module)

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

    # do backup and fetch response (which is the backup) (catch error here)
    do_backup_response = None
    try:
        do_backup_response = package_instance.do_backup()
    except Exception as error:
        print(f"error: ", error)
        backup_execution.state = 2
        backup_execution.errors = error

    # end the backup_execution
    backup_execution.ends_at = now()
    backup_execution.state = 3
    backup_execution.output = do_backup_response
    backup_execution.save()

    # create backup
    Backup.objects.create(name=f"backup for {backup_job.name}, {do_backup_response}", backup_job=backup_job)

    # TODO: Store the result with the store_modules (import it in the paramters) (loop for all store_modules)
    # in loop create a module_instance, inject secrets and params, create a storage_execution,
    # create the backup and save it with the store_module, create the backup object, and end the storage_execution

