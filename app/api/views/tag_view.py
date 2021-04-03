from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .base_view import BaseViewSet
from ..exceptions import MessageStatusCodeException, AppErrorException
from ..rms_base import RmsBaseViewSetFilter
from ..serializers import *
from ..models import Tag
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language as get_language
import os

User = get_user_model()

class TagViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = Tag
        fields = Tag.filterset_fields

class TagViewSet(BaseViewSet):
    serializer_class = TagPostSerializer
    model_class = Tag
    filterset_class = TagViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return TagRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return TagPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return TagListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(TagViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return Tag.objects.all()

    @action(detail=False, methods=['get'], url_path='own',
            permission_classes=(IsAuthenticated,))
    def own(self, request, *args, **kwargs):
        list = self.paginate_queryset(self.get_queryset().filter(created_by=request.user))
        serializer = self.get_serializer_list_class()(list, many=True)
        return self.get_paginated_response(serializer.data)
