from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import BackupModule
from django.contrib.auth import get_user_model
from ..serializers.backup_module_serializer import *

User = get_user_model()



class BackupModuleViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = BackupModule
        fields = BackupModule.filterset_fields

class BackupModuleViewSet(BaseViewSet):
    serializer_class = BackupModulePostSerializer
    model_class = BackupModule
    filterset_class = BackupModuleViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return BackupModuleRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return BackupModulePostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return BackupModuleListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(BackupModuleViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return BackupModule.objects.all()

