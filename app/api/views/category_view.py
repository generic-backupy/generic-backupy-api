from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import Category
from django.contrib.auth import get_user_model
from ..serializers.category_serializer import *

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
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(CategoryViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return Category.objects.all()

