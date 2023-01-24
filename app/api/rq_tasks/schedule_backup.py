import datetime

from django_rq import job
from api.models import Backup, BackupExecution, BackupJob, User
from api.models import BackupSchedule
from django.utils.timezone import now
from api.utils.package_util import PackageUtil
from ..utils.backup_util import *


@job
def schedule(backup_job: BackupJob, user: User, schedule: BackupSchedule):
    # do backup
    if schedule.next_start:
        schedule.last_start = schedule.next_start
        schedule.next_start = datetime.datetime.fromtimestamp(schedule.next_start.timestamp() + schedule.each_nth_minute)
        schedule.save()
    BackupUtil.do_backup(backup_job, user)

