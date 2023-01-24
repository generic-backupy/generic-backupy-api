from django.utils.datetime_safe import datetime
from rest_framework.decorators import action
from rest_framework.response import Response

from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import BackupSchedule
from django.contrib.auth import get_user_model
from ..serializers.backup_schedule_serializer import *

User = get_user_model()
from django_rq.queues import get_queue


class BackupScheduleViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = BackupSchedule
        fields = BackupSchedule.filterset_fields

class BackupScheduleViewSet(BaseViewSet):
    serializer_class = BackupSchedulePostSerializer
    model_class = BackupSchedule
    filterset_class = BackupScheduleViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return BackupScheduleRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return BackupSchedulePostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return BackupScheduleListSerializer

    def perform_create(self, serializer):
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(BackupScheduleViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return BackupSchedule.objects.all()


