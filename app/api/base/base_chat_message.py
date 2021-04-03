from django.db import models
from api.base import BaseModel
from django.conf import settings


class BaseChatMessage(BaseModel):
    message = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   default=None,
                                   blank=True,
                                   on_delete=models.SET_NULL,
                                   null=True)

    # filter
    search_fields = ['message']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def __str__(self):
        return "{} - {}".format(self.id, self.message)
