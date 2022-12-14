from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import StorageExecution
from django.contrib.auth import get_user_model
from ..serializers.storage_execution_serializer import *

User = get_user_model()



class StorageExecutionViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = StorageExecution
        fields = StorageExecution.filterset_fields

class StorageExecutionViewSet(BaseViewSet):
    serializer_class = StorageExecutionPostSerializer
    model_class = StorageExecution
    filterset_class = StorageExecutionViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return StorageExecutionRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return StorageExecutionPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return StorageExecutionListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(StorageExecutionViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return StorageExecution.objects.all()

