from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings


"""
ModelClass for a System, which should be managed by generic-backupy (switches, routers, databases, etc.)
"""
class System(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    # ip address/domain like 10.10.10.2, router.local, db.test.com
    host = models.TextField()
    additional_information = models.TextField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL,
                                 blank=True, related_name='system_category')

    # filter
    search_fields = ['name']
    ordering_fields = ['id']
    ordering = ['-id']

    def __str__(self):
        return f"{self.id} - {self.name}"
