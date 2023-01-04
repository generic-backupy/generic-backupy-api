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

Secrets: The secrets will be used from the system itself. So if the storage_module isn't in the 
storage_modules of the system anymore
The store (and restore) process will not work.
"""
class Backup(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    path = models.TextField(null=True, blank=True)
    original_file_name = models.TextField(null=True, blank=True)
    backup_job = models.ForeignKey('BackupJob', null=True, on_delete=models.SET_NULL,
                               blank=True, related_name='backup_category')
    backup_module = models.ForeignKey('BackupModule', null=True, on_delete=models.SET_NULL,
                                      blank=True, related_name='backup_backup_module')
    backup_job_storage_module = models.ForeignKey('BackupJobStorageModule', null=True, on_delete=models.SET_NULL,
                                       blank=True, related_name='backup_backup_job_storage_module')

    additional_parameters = models.JSONField(null=True, blank=True)
    backup_execution = models.ForeignKey('BackupExecution', null=True, blank=True, on_delete=models.SET_NULL)
    storage_execution = models.ForeignKey('StorageExecution', null=True, blank=True, on_delete=models.SET_NULL)

    # filter
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.name}"
