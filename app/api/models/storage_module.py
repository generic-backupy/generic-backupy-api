from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings

"""
ModelClass for a StorageModule, which is responsible for store the backup data (local storage, cloud, etc.)
"""
class StorageModule(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    # link to the folder like module /opt/data/modules/any-module/gb_module.py
    # the file_system_path would be /opt/data/modules/any-module
    file_system_path = models.TextField()
    module_config = models.JSONField(null=True, blank=True, default=None)

    # filter
    search_fields = ['name']
    ordering_fields = ['id']
    ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.name}"
