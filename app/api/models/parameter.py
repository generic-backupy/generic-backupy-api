from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings


class Parameter(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    parameter = models.JSONField()

    # filter
    search_fields = ['name']
    ordering_fields = ['id']
    ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.name}"
