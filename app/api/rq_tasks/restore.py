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
def restore(backup: Backup, user, restore_execution):
    # start a restore_execution
    restore_execution.state = 1
    restore_execution.save()
    backup_job = backup.backup_job

    # first restore it from storage



    # afterwards restore the system with the loaded backup

    package_instance = PackageUtil.get_package_instance_or_error(restore_execution, backup_job.backup_module)
    do_backup_response = None

    if package_instance:
        # inject the parameters etc.
        PackageUtil.inject_backup_parameters(package_instance, backup_job, backup.additional_parameters)

        # inject the log function
        PackageUtil.inject_module_log_function(package_instance, restore_execution)

        # do backup and fetch response (which is a backup_result type)
        try:
            do_backup_response = package_instance.do_backup()
        except Exception as error:
            print(f"error: ", error)
            restore_execution.state = 2
            restore_execution.errors = error

    # end the restore_execution
    restore_execution.ends_at = now()
    restore_execution.state = 3
    if not do_backup_response or do_backup_response.error:
        restore_execution.state = 2
        if do_backup_response:
            restore_execution.errors = (restore_execution.errors or "") + (do_backup_response.error or "")
        elif not restore_execution.errors:
            restore_execution.errors = "UNKNOWN ERROR"
    if do_backup_response:
        restore_execution.output = do_backup_response.output
    restore_execution.save()

    # return if we had an error
    if restore_execution.state == 2:
        return
