from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import Secret
from django.contrib.auth import get_user_model
from ..serializers.secret_serializer import *

User = get_user_model()



class SecretViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = Secret
        fields = Secret.filterset_fields

class SecretViewSet(BaseViewSet):
    serializer_class = SecretPostSerializer
    model_class = Secret
    filterset_class = SecretViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return SecretRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return SecretPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return SecretListSerializer

    def perform_create(self, serializer):
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(SecretViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return Secret.objects.all()

