from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..serializers.backup_job_serializer import *
from ..models import BackupJob
from django.contrib.auth import get_user_model
from ..utils.backup_util import BackupUtil

User = get_user_model()



class BackupJobViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = BackupJob
        fields = BackupJob.filterset_fields

class BackupJobViewSet(BaseViewSet):
    serializer_class = BackupJobPostSerializer
    model_class = BackupJob
    filterset_class = BackupJobViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return BackupJobRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return BackupJobPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return BackupJobListSerializer

    def perform_create(self, serializer):
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(BackupJobViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return BackupJob.objects.all()

    @action(detail=True, methods=['get'], url_path='execute/backup',
            permission_classes=(IsAuthenticated,))
    def execute_backup(self, request, *args, **kwargs):
        backup_job = self.get_object()
        execute_async = request.GET.get('execute-async', 'True').lower() in ['1', 'true']
        BackupUtil.do_backup(backup_job, self.request.user, execute_async=execute_async)

        return Response(None, 200)

