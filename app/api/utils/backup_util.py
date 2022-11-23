from api.exceptions import AppErrorException
from api.models import BackupJob, BackupJobStorageModule
from api.utils.package_util import PackageUtil

from ..rq_tasks.backup import *

"""
Provides an interface, to hide the implementation for rq (func.delay(..)), to switch it later if needed
"""
class BackupUtil:

    @staticmethod
    def do_backup(backup_job: BackupJob, user):
        backup_module = backup_job.backup_module

        # raise error if no backup_module is specified
        if not backup_module:
            raise AppErrorException("No Backup Module",
                                    "There is no backup module specified for this job", status_code=400)

        backup_job_storage_modules = BackupJobStorageModule.objects.filter(backup_job=backup_job)

        # raise error if there is no storage module
        if not backup_job_storage_modules or len(backup_job_storage_modules) < 1:
            raise AppErrorException("No Storage Module",
                            "There is no storage module specified for this job, "
                            "you need at least one storage module", status_code=400)

        backup.delay(backup_job, backup_module, backup_job_storage_modules, user)
