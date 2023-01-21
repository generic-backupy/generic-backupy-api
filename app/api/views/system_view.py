from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import System
from django.contrib.auth import get_user_model
from ..serializers.system_serializer import *

User = get_user_model()



class SystemViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = System
        fields = System.filterset_fields

class SystemViewSet(BaseViewSet):
    serializer_class = SystemPostSerializer
    model_class = System
    filterset_class = SystemViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return SystemRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return SystemPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return SystemListSerializer

    def perform_create(self, serializer):
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(SystemViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return System.objects.all()

