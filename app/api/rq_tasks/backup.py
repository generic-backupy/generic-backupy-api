from django_rq import job
import django_rq
from api.models import Backup, BackupJob
import time

from api.utils.package_util import PackageUtil


@job
def backup(backup_job: BackupJob, backup_module):
    # get an instance of the plugin
    package_instance = PackageUtil.get_python_class_of_module(backup_module)()

    # inject the secrets

    # inject the params

    # start a backup_execution

    # do backup and fetch response (which is the backup)
    do_backup_response = package_instance.do_backup()

    # end the backup_execution

    # create backup
    Backup.objects.create(name=f"backup for {backup_job.name}, {do_backup_response}", backup_job=backup_job)

    # TODO: Store the result with the store_modules (import it in the paramters) (loop for all store_modules)
    # in loop create a module_instance, inject secrets and params, create a storage_execution,
    # create the backup and save it with the store_module, create the backup object, and end the storage_execution

