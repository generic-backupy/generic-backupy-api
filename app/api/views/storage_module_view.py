from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import StorageModule
from django.contrib.auth import get_user_model
from ..serializers.storage_module_serializer import *

User = get_user_model()



class StorageModuleViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = StorageModule
        fields = StorageModule.filterset_fields

class StorageModuleViewSet(BaseViewSet):
    serializer_class = StorageModulePostSerializer
    model_class = StorageModule
    filterset_class = StorageModuleViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return StorageModuleRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return StorageModulePostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return StorageModuleListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(StorageModuleViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return StorageModule.objects.all()

