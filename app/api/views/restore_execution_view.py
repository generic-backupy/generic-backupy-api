from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import RestoreExecution
from django.contrib.auth import get_user_model
from ..serializers.restore_execution_serializer import *

User = get_user_model()



class RestoreExecutionViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = RestoreExecution
        fields = RestoreExecution.filterset_fields

class RestoreExecutionViewSet(BaseViewSet):
    serializer_class = RestoreExecutionPostSerializer
    model_class = RestoreExecution
    filterset_class = RestoreExecutionViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return RestoreExecutionRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return RestoreExecutionPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return RestoreExecutionListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(RestoreExecutionViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return RestoreExecution.objects.all()

