from django.db import models

from ..base import BaseModel
from django.conf import settings

from ..utils.ExecutionUtil import ExecutionUtil

"""
ModelClass for a execution of a specific BackupJob (backup or restore)
"""
class RestoreExecution(BaseModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    # will be filled after the execution (not matter if it was an error or a success)
    ends_at = models.DateTimeField(null=True, blank=True)
    # marks the state of the execution (waiting=0, running=1, error=2, success=3)
    state = models.IntegerField(default=0)
    # output of the execution
    output = models.TextField(null=True, blank=True)
    # logs of the execution
    logs = models.TextField(null=True, blank=True)
    # errors of the execution
    errors = models.TextField(null=True, blank=True)
    # backup
    backup_instance = models.ForeignKey('Backup', on_delete=models.SET_NULL, null=True, blank=True)

    # filter
    search_fields = []
    ordering_fields = ['id']
    ordering = ['-id']

    def __str__(self):
        if self.backup_instance is not None:
            return f"{self.id} - {ExecutionUtil.get_state_string(self.state)}" \
                   f" - {self.backup_instance.name}"
        else:
            return f"{self.id} - {ExecutionUtil.get_state_string(self.state)}"

