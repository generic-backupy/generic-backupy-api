from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .push_token import PushToken
from ..utils.push_notification_util import PushNotificationUtil
from django.utils.crypto import get_random_string
from django.utils.timezone import datetime


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=128, default=None, null=True, blank=True, unique=True)
    email_verification_code_created_at = models.DateTimeField(null=True, default=None, blank=True)
    email_verification_code_accepted_at = models.DateTimeField(null=True, default=None, blank=True)
    email_verification_code_last_request = models.DateTimeField(null=True, default=None, blank=True)
    reset_password_code_last_request = models.DateTimeField(null=True, default=None, blank=True)
    privacy_version = models.CharField(null=True, default=None, blank=True, max_length=6)
    last_privacy_check = models.DateTimeField(null=True, default=None, blank=True)
    conditions_version = models.CharField(null=True, default=None, blank=True, max_length=6)
    last_conditions_check = models.DateTimeField(null=True, default=None, blank=True)
    created_with_user_agent = models.TextField(null=True, default=None, blank=True)
    created_language = models.CharField(max_length=10, default="en")

    # filter
    search_fields = ['username']
    ordering_fields = ['username']
    ordering = ['username']
    filterset_fields = []

    def create_email_verification_code(self, save=True):
        now = datetime.now(timezone.utc)
        verification_code = get_random_string(length=32)

        # retry if code already exist
        if User.objects.filter(email_verification_code=verification_code).exists():
            return self.create_email_verification_code()

        self.email_verification_code = verification_code
        self.email_verification_code_created_at = now
        if (save):
            self.save()
        return (verification_code, now)

    def send_push_notification(self, **kwargs):
        return PushNotificationUtil.sendToUser(self, **kwargs)

    def get_push_tokens(self):
        tokens = PushToken.objects.filter(auth_token__user=self).values_list('key', flat=True)
        return tokens
