from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings

"""
ModelClass for a Category, which acts like a folder, which can have subfolders etc.
"""
class Category(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    parent = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, blank=True)

    # filter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def __str__(self):
        return f"{self.id} - {self.name}"
