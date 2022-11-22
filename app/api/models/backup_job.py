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
    # secrets which should be injected to the backup module
    backup_module_secrets = models.ManyToManyField('Secret', through="BackupJobSecret", related_name="backup_job_secret")
    # TODO: also add properties to the the secrets and the backup_job, which can be used by the module (like params like encrypt, etc.)
    # TODO: also add default encryption feature for modules (in the BaseModule) to make it easy to encrypt backups
    # because there are multiple storage_modules, we get multiple backup objects. One for each storage module (because of different paths, etc.)
    storage_modules = models.ManyToManyField('StorageModule', through="BackupJobStorageModule", related_name="backup_job_storage_modules")

    # filter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def __str__(self):
        return f"{self.id} - {self.name}"


class BackupJobSecret(BaseModel):
    backup_job = models.ForeignKey(BackupJob, on_delete=models.CASCADE, related_name="backup_job_secret_backup_job")
    secret = models.ForeignKey('Secret', on_delete=models.CASCADE, related_name="backup_job_secret_secret")

    def __str__(self):
        return f"{self.id} - {self.backup_job.name}/{self.secret.name}"


class BackupJobStorageModule(BaseModel):
    backup_job = models.ForeignKey(BackupJob, on_delete=models.CASCADE, related_name="backup_job_storage_module_backup_job")
    storage_module = models.ForeignKey('StorageModule', on_delete=models.CASCADE, related_name="backup_job_storage_module_storage_module")
    secrets = models.ManyToManyField('Secret', through="BackupJobStorageModuleSecret", related_name="backup_job_storage_module_secret")

    def __str__(self):
        return f"{self.id} - {self.backup_job.name}/{self.storage_module}"


class BackupJobStorageModuleSecret(BaseModel):
    backup_job_storage_module = models.ForeignKey(BackupJobStorageModule,
                                                  on_delete=models.CASCADE,
                                                  related_name="backup_job_storage_module_secret_backup_job_storage_module")
    secret = models.ForeignKey('Secret', on_delete=models.CASCADE, related_name="backup_job_storage_model_secret_secret")

    def __str__(self):
        return f"{self.id} - {self.backup_job_storage_module.backup_job.name}/{self.secret.name}"
