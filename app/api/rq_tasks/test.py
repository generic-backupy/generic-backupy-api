from django_rq import job
from api.models import Backup, BackupExecution, BackupJob
from django.utils.timezone import now
from api.utils.package_util import PackageUtil


@job
def test():
    # start a restore_execution
    BackupExecution.objects.create(state=3, logs="test", backup_job=BackupJob.objects.first())

