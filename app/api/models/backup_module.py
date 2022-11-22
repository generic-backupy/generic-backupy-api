from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings

"""
ModelClass for a BackupModule, which is responsible for backup and restore processes
"""
class BackupModule(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    # link to the folder like module /opt/data/modules/any-module/gb_module.py
    # the file_system_path would be /opt/data/modules/any-module
    file_system_path = models.TextField()

    # filter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def __str__(self):
        return f"{self.id} - {self.name}"
