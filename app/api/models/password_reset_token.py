from django.db import models
from ..base import BaseModel
from django.conf import settings


class PasswordResetToken(BaseModel):
    token = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   blank=True,
                                   on_delete=models.SET_NULL,
                                   null=True)

    # filter
    search_fields = ['token']
    ordering_fields = ['token']
    ordering = ['created_at']

    def __str__(self):
        return "{} - {}".format(self.id, self.token)
