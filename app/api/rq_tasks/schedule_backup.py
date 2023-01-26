import datetime

from django_rq import job
from api.models import Backup, BackupExecution, BackupJob, User
from api.models import BackupSchedule
from django.utils.timezone import now
from api.utils.package_util import PackageUtil
from ..utils.backup_util import *


@job
def schedule(schedule: BackupSchedule):
    # reload schedule from database, because the object probably changed in the meanwhile
    schedule.refresh_from_db()

    # fetch backup job and user
    backup_job = schedule.backup_job
    user = schedule.created_by

    # calculate next start
    if schedule.next_start:
        schedule.last_start = schedule.next_start
        schedule.next_start = datetime.datetime.fromtimestamp(schedule.next_start.timestamp() + schedule.each_nth_minute)
        schedule.save()

    # do backup
    BackupUtil.do_backup(backup_job, user)

