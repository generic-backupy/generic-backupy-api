from api.exceptions import AppErrorException
from api.models import BackupJob
from api.utils.package_util import PackageUtil
from ..rq_tasks.backup import *

"""
Provides an interface, to hide the implementation for rq (func.delay(..)), to switch it later if needed
"""
class BackupUtil:

    @staticmethod
    def do_backup(backup_job: BackupJob):
        backup_module = backup_job.backup_module

        # return if no backup_module is specified
        if not backup_module:
            raise AppErrorException("No Backup Module",
                                    "There is no backup module specified for this job", status_code=400)

        backup.delay(backup_job, backup_module)
