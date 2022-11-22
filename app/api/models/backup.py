from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings


"""
ModelClass for a Backup, which is located in any storage place (depends on the storage module)
We also save the backup_module and the storage_module here (so we have it duplicated in backup job and in backup), 
for the case, the modules in the backup_job will be changed. 
The backup/storage modules in the backup_job are only used for new backups, and not for restoring, etc.
"""
class Backup(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    backup_job = models.ForeignKey('BackupJob', null=True, on_delete=models.SET_NULL,
                               blank=True, related_name='backup_category')
    backup_module = models.ForeignKey('BackupModule', null=True, on_delete=models.SET_NULL,
                                      blank=True, related_name='backup_backup_module')
    storage_module = models.ForeignKey('StorageModule', null=True, on_delete=models.SET_NULL,
                                       blank=True, related_name='backup_storage_module')

    # filter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def __str__(self):
        return f"{self.id} - {self.name}"
