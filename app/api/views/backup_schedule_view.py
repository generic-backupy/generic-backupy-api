from django.utils.datetime_safe import datetime
from rest_framework.decorators import action
from rest_framework.response import Response

from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import BackupSchedule
from django.contrib.auth import get_user_model
from ..serializers.backup_schedule_serializer import *

User = get_user_model()
from api.rq_tasks.test import test
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

    @action(detail=False, methods=['get'], url_path='test')
    def test(self, request, *args, **kwargs):

        queue = get_queue('default')
        job = queue.enqueue_at(datetime(2023, 1, 24, 15, 36), test)
        job_id = job.id #str
        return Response("hey")


