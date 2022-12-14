from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import Backup
from django.contrib.auth import get_user_model
from ..serializers.backup_serializer import *

User = get_user_model()



class BackupViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = Backup
        fields = Backup.filterset_fields

class BackupViewSet(BaseViewSet):
    serializer_class = BackupPostSerializer
    model_class = Backup
    filterset_class = BackupViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return BackupRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return BackupPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return BackupListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(BackupViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return Backup.objects.all()

