from api.models import BackupJob
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import Category
from django.contrib.auth import get_user_model
from ..serializers.category_serializer import *
from ..utils.backup_util import BackupUtil
from ..utils.category_util import CategoryUtil

User = get_user_model()



class CategoryViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = Category
        fields = Category.filterset_fields

class CategoryViewSet(BaseViewSet):
    serializer_class = CategoryPostSerializer
    model_class = Category
    filterset_class = CategoryViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return CategoryRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return CategoryPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return CategoryListSerializer

    def perform_create(self, serializer):
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(CategoryViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return Category.objects.all()


    @action(detail=True, methods=['get'], url_path='execute/backup',
            permission_classes=(IsAuthenticated,))
    def execute_backup(self, request, *args, **kwargs):
        current_category = self.get_object()

        # fetch all categories (selected and childs)
        categories = CategoryUtil.get_child_categories(current_category)

        for backup_job in BackupJob.objects.filter(system__category__in=categories).distinct():
            BackupUtil.do_backup(backup_job, self.request.user)

        return Response(None, 200)
