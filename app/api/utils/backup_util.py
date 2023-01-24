from api.exceptions import AppErrorException
from api.models.restore_execution import RestoreExecution
from api.models.backup_execution import BackupExecution
from api.models.backup_job import BackupJob
from api.utils.package_util import PackageUtil
from ..rq_tasks.restore import restore

from ..rq_tasks.backup import *
from django_rq.queues import get_queue

"""
Provides an interface, to hide the implementation for rq (func.delay(..)), to switch it later if needed
"""
class BackupUtil:

    @staticmethod
    def do_backup(backup_job: BackupJob, user, execute_async=True, at_time=None):
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

        backup_execution = BackupExecution.objects.create(created_by=user, backup_job=backup_job, backup_module=backup_module)
        backup_func = backup
        if execute_async:
            backup_func = backup.delay

        if at_time:
            queue = get_queue('default')
            return queue.enqueue_at(at_time, backup)
        return backup_func(backup_job, backup_module, backup_job_storage_modules, user, backup_execution)

    @staticmethod
    def do_restore(backup_obj: Backup, user, execute_async=True):
        restore_execution = RestoreExecution.objects.create(created_by=user, backup_instance=backup_obj)
        restore_func = restore
        if execute_async:
            restore_func = restore.delay
        restore_func(backup_obj, user, restore_execution)
