from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from ..base import BaseModel


class Secret(BaseModel):
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   on_delete=models.CASCADE,
                                   null=True)
    # TODO: needs to be obfuscate later (encrypt/decrypt with a secret key,
    #  to prevent direct access at database leak, or other solutions)
    #  unfortunately we can't encrypt/decrypt it with the user password, because then
    #  it is not possible to use automated backups, because for that we need the real password for example
    secret = models.TextField()

    # filter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def __str__(self):
        return f"{self.id} - {self.name}"
