from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings


"""
ModelClass for a execution of a specific BackupJob (backup or restore)
"""
class BackupExecution(BaseModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    # will be filled after the execution (not matter if it was an error or a success)
    ends_at = models.DateTimeField(null=True, blank=True)
    # marks the state of the execution (running=1, error=2, success=3)
    state = models.IntegerField(default=1)
    # output of the execution
    output = models.TextField(null=True, blank=True)
    # logs of the execution
    logs = models.TextField(null=True, blank=True)
    # errors of the execution
    errors = models.TextField(null=True, blank=True)
    # backup job
    backup_job = models.ForeignKey('BackupJob', on_delete=models.CASCADE)
    # backup module
    backup_module = models.ForeignKey('BackupModule', on_delete=models.SET_NULL, null=True, blank=True)

    # filter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def __str__(self):
        return f"{self.id} - {'Running' if self.state == 1 else ('Error' if self.state == 2 else 'Success')}" \
               f" - {self.backup_job.name}"
