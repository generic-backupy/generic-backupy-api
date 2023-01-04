from django_rq import job
from api.models import Backup
from django.utils.timezone import now
from api.utils.package_util import PackageUtil


@job
def restore(backup: Backup, user, restore_execution):
    # start a restore_execution
    restore_execution.state = 1
    restore_execution.save()
    backup_job = backup.backup_job

    # first restore it from storage
    storage_package_instance = PackageUtil.get_package_instance_or_error(restore_execution, backup.backup_job_storage_module.storage_module)
    do_retrieve_response = None

    if storage_package_instance:
        # inject the parameters etc.
        PackageUtil.inject_backup_parameters(storage_package_instance, backup_job, backup.additional_parameters)

        # inject the log function
        PackageUtil.inject_module_log_function(storage_package_instance, restore_execution)

        # inject the retrieve path
        storage_package_instance.retrieve_path = backup.path

        # do backup and fetch response (which is a backup_result type)
        try:
            do_retrieve_response = storage_package_instance.retrieve_from_storage()
        except Exception as error:
            print(f"error: ", error)
            restore_execution.state = 2
            restore_execution.errors = error

    # if there was an error at retrieving, stop and return with an error
    if PackageUtil.handle_error_if_exist(do_retrieve_response, restore_execution):
        return

    # if retrieve action was successfully, pass the backup to the backup module, and restore it

    package_instance = PackageUtil.get_package_instance_or_error(restore_execution, backup.backup_module)
    do_restore_response = None

    if package_instance:
        # inject the parameters etc.
        PackageUtil.inject_backup_parameters(package_instance, backup_job, backup.additional_parameters)

        # inject the log function
        PackageUtil.inject_module_log_function(package_instance, restore_execution)

        # do backup and fetch response (which is a backup_result type)
        try:
            do_restore_response = package_instance.do_restore(None)
        except Exception as error:
            print(f"error: ", error)
            restore_execution.state = 2
            restore_execution.errors = error

    # end the restore_execution
    restore_execution.ends_at = now()
    restore_execution.state = 3
    if PackageUtil.handle_error_if_exist(do_restore_response, restore_execution):
        return
