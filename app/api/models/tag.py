from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel
from django.conf import settings


class Tag(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)

    # filter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def __str__(self):
        return "{} - {}".format(self.id, self.name)

    @staticmethod
    def check_duplicate(name, created_by):
        return Tag.objects.filter(Q(name=name, created_by=created_by)).exists()

    def clean(self):
        if Tag.check_duplicate(self.name, self.created_by):
            raise ValidationError("Duplicate!")
        super(Tag, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        super(Tag, self).save(*args, **kwargs)
