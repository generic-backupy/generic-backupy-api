from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import Parameter
from django.contrib.auth import get_user_model
from ..serializers.parameter_serializer import *

User = get_user_model()



class ParameterViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = Parameter
        fields = Parameter.filterset_fields

class ParameterViewSet(BaseViewSet):
    serializer_class = ParameterPostSerializer
    model_class = Parameter
    filterset_class = ParameterViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return ParameterRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return ParameterPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return ParameterListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(ParameterViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return Parameter.objects.all()

