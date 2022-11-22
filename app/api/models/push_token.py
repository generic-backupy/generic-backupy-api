from django.db import models
from ..base import BaseModel
from knox.models import AuthToken


class PushToken(BaseModel):
    key = models.TextField(unique=True)
    auth_token = models.ForeignKey(AuthToken, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.auth_token.user.username} - {self.key}"
