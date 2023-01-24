from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings

"""
ModelClass for a Backup Schedule, to schedule backupjobs
"""
class BackupSchedule(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    each_nth_minute = models.IntegerField(default=60*60*24) # default each day
    next_start = models.DateTimeField(null=True, default=True, blank=True) # next start time
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
