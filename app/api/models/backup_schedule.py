import datetime
import time

from .backup_job import BackupJobStorageModule
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django_rq.queues import get_queue
from ..base import BaseModel
from django.conf import settings
from .backup_execution import BackupExecution


"""
ModelClass for a Backup Schedule, to schedule backupjobs
"""
class BackupSchedule(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    each_nth_minute = models.IntegerField(default=60*60*24) # default each day
    next_start = models.DateTimeField(null=True, blank=True) # next start time
    last_start = models.DateTimeField(null=True, blank=True) # last start time
    disabled = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    current_scheduling_job_id = models.TextField(null=True, default=True, blank=True)
    backup_job = models.ForeignKey('BackupJob', on_delete=models.CASCADE, related_name='backup_schedule_backup_job')

    # filter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def __str__(self):
        return f"{self.id} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.pk: # create
            super(BackupSchedule, self).save(*args, **kwargs)
            if not self.next_start:
                self.next_start = datetime.datetime.fromtimestamp(time.time() + self.each_nth_minute)
            job = self.create_scheduled_rq_job(self.next_start)
            if not job:
                self.next_start = None
            else:
                self.current_scheduling_job_id = job.id
            self.save()
        else: # update
            # remove rq job if disabled
            if (self.disabled != self.initial_model.get("disabled")) and self.disabled:
                self.remove_qr_job()
            # renew rq job if time changed
            if (self.next_start != self.initial_model.get("next_start")):
                self.remove_qr_job()
                self.current_scheduling_job_id = self.create_scheduled_rq_job(self.next_start).id
            super(BackupSchedule, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.current_scheduling_job_id:
            self.remove_qr_job()
        super(BackupSchedule, self).save(using, keep_parents)

    def create_scheduled_rq_job(self, at_time):
        from api.rq_tasks.schedule_backup import schedule
        queue = get_queue('default')
        return queue.enqueue_at(at_time, schedule, self.backup_job, self.created_by, self)

    def remove_qr_job(self):
        queue = get_queue('default')
        try:
            queue.remove(self.current_scheduling_job_id)
        except Exception as e:
            print(f"ERROR: {e}")
