from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings


"""
ModelClass for a BackupJob for one system
"""
class BackupJob(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    additional_information = models.TextField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    system = models.ForeignKey('System', null=True, on_delete=models.SET_NULL,
                                 blank=True, related_name='backup_job_category')
    backup_module = models.ForeignKey('BackupModule', null=True, on_delete=models.SET_NULL,
                                      blank=True, related_name='backup_job_backup_module')
    storage_module = models.ForeignKey('StorageModule', null=True, on_delete=models.SET_NULL,
                                       blank=True, related_name='backup_job_storage_module')

    # filter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def __str__(self):
        return f"{self.id} - {self.name}"
