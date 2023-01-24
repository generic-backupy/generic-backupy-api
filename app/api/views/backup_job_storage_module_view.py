from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import BackupJobStorageModule
from django.contrib.auth import get_user_model
from ..serializers.backup_job_storage_module_serializer import *

User = get_user_model()



class BackupJobStorageModuleViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = BackupJobStorageModule
        fields = BackupJobStorageModule.filterset_fields

class BackupJobStorageModuleViewSet(BaseViewSet):
    serializer_class = BackupJobStorageModulePostSerializer
    model_class = BackupJobStorageModule
    filterset_class = BackupJobStorageModuleViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return BackupJobStorageModuleRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return BackupJobStorageModulePostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return BackupJobStorageModuleListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(BackupJobStorageModuleViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return BackupJobStorageModule.objects.all()

