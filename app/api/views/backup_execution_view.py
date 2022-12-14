from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import BackupExecution
from django.contrib.auth import get_user_model
from ..serializers.backup_execution_serializer import *

User = get_user_model()



class BackupExecutionViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = BackupExecution
        fields = BackupExecution.filterset_fields

class BackupExecutionViewSet(BaseViewSet):
    serializer_class = BackupExecutionPostSerializer
    model_class = BackupExecution
    filterset_class = BackupExecutionViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return BackupExecutionRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return BackupExecutionPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return BackupExecutionListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(BackupExecutionViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return BackupExecution.objects.all()

