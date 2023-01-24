from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings

from ..utils.ExecutionUtil import ExecutionUtil

"""
ModelClass for a execution of a installation process
"""
class ModuleInstallationExecution(BaseModel):
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
    # installed backup module
    backup_module = models.ForeignKey('BackupModule', on_delete=models.SET_NULL, null=True, blank=True)
    # installed backup module
    storage_module = models.ForeignKey('StorageModule', on_delete=models.SET_NULL, null=True, blank=True)

    # filter
    search_fields = []
    ordering_fields = []
    ordering = []

    def __str__(self):
        return f"{self.id} - {ExecutionUtil.get_state_string(self.state)}" \
               f""

    def log(self, message):
        if self.logs == None:
            self.logs = ""
        self.logs += f"{message}\n"
        self.save()
