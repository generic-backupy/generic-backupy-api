from django.core.exceptions import FieldError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework import filters
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import BasePermission, IsAuthenticated

from api.base import BaseModel
from api.exceptions import MessageStatusCodeException, AppErrorException
from api.utils.app_info import AppInfo

class RmsBaseViewSetPermission(BasePermission):

    def has_permission(self, request, view, *args, **kwargs):
        """raise AppErrorException({
            "post": view.has_permission_post(),
            "create": view.has_permission_create(),
            "get": view.has_permission_get()
            #"put": view.has_permission_put(),
            #"patch": view.has_permission_patch()
        })"""

        if not view.has_permission():
            return False

        # http methods
        if request.method == 'GET' and not view.has_permission_get():
            return False
        if request.method == 'POST' and not view.has_permission_post():
            return False
        if request.method == 'PUT' and not view.has_permission_put():
            return False
        if request.method == 'PATCH' and not view.has_permission_patch():
            return False
        if request.method == 'OPTIONS' and not view.has_permission_options():
            return False
        if request.method == 'DELETE' and not view.has_permission_delete():
            return False

        # rest actions
        if view.action == 'create' and not view.has_permission_create():
            return False
        if view.action == 'update' and not view.has_permission_update():
            return False
        if view.action == 'partial_update' and not view.has_permission_partial_update():
            return False
        if view.action == 'list' and not view.has_permission_list():
            return False
        if view.action == 'retrieve' and not view.has_permission_retrieve():
            return False
        if view.action == 'head' and not view.has_permission_head():
            return False

        return True


class RmsBaseViewSetFilter(filters.FilterSet):

    own = filters.BooleanFilter(field_name='created_by', method='method_own')

    def method_own(self, queryset, name, value):
        if value:
            try:
                return queryset.filter(created_by=self.request.user)
            except FieldError:
                return queryset
        return queryset

    class Meta:
        model = BaseModel
        fields = BaseModel.filterset_fields

class RmsBaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'options', 'delete', ]
    permission_classes = (IsAuthenticated, RmsBaseViewSetPermission)
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    model_class: BaseModel = None
    search_fields = []
    ordering_fields = []
    ordering = []
    filterset_fields = []
    should_use_additional_permission_classes = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_fields = self.get_search_fields()
        self.ordering_fields = self.get_ordering_fields()
        self.ordering = self.get_ordering()
        self.filterset_fields = self.get_filterset_fields()
        if self.get_additional_permission_classes() and self.permission_classes and self.should_use_additional_permission_classes:
            self.permission_classes = self.permission_classes + self.get_additional_permission_classes()
        if self.permission_classes is None:
            self.permission_classes = ()

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        super(RmsBaseViewSet, self).perform_create(serializer)

    def get_additional_permission_classes(self):
        return None

    def add_field_to_serializer(self, serializer, field_name, field_value):
        serializer._validated_data[field_name] = field_value

    def add_user_agent_to_serializer(self, serializer):
        self.add_field_to_serializer(serializer, "created_with_user_agent", self.get_user_agent())

    def get_user_agent(self):
        return self.request.META['HTTP_USER_AGENT']

    def is_detail_action(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        return lookup_url_kwarg in self.kwargs

    def get_filterset_fields(self):
        if self.model_class:
            return self.model_class.filterset_fields
        return self.filterset_fields

    def get_search_fields(self):
        if self.model_class:
            return self.model_class.search_fields
        return self.search_fields

    def get_ordering_fields(self):
        if self.model_class:
            return self.model_class.ordering_fields
        return self.ordering_fields

    def get_ordering(self):
        if self.model_class:
            return self.model_class.ordering
        return self.ordering

    def get_serializer_create_class(self, *args, **kwargs):
        return None

    def get_serializer_update_class(self, *args, **kwargs):
        return None

    def get_serializer_partial_update_class(self, *args, **kwargs):
        return None

    def get_serializer_list_class(self, *args, **kwargs):
        return None

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return None

    def get_serializer_head_class(self, *args, **kwargs):
        return None

    def get_serializer_class(self, *args, **kwargs):
        c_serializer = self.get_serializer_create_class(*args, **kwargs)
        if self.action == 'create' and c_serializer:
            return c_serializer
        c_serializer = self.get_serializer_update_class(*args, **kwargs)
        if self.action == 'update' and c_serializer:
            return c_serializer
        c_serializer = self.get_serializer_partial_update_class(*args, **kwargs)
        if self.action == 'partial_update' and c_serializer:
            return c_serializer
        c_serializer = self.get_serializer_list_class(*args, **kwargs)
        if self.action == 'list' and c_serializer:
            return c_serializer
        c_serializer = self.get_serializer_retrieve_class(*args, **kwargs)
        if self.action == 'retrieve' and c_serializer:
            return c_serializer
        c_serializer = self.get_serializer_head_class(*args, **kwargs)
        if self.action == 'head' and c_serializer:
            return c_serializer
        return super().get_serializer_class(*args, **kwargs)

    def get_param_or_none_from_request(self, request, name):
        field = request.GET.getlist(name)

        if len(field) > 0 and len(field[0]) > 0:
            return field[0]

        return None

    def get_bool_or_none_from_request(self, request, name):
        val = self.get_param_or_none_from_request(request, name)
        if val:
            return val.lower() in ['1', 'true', 'yes']
        return None

    # get the name of the current endpoint
    def get_endpoint(self):
        return [x for x in self.request.path.split("/") if len(x) > 0][-1]

    def has_permission(self):
        return True

    def has_permission_get(self):
        return True

    def has_permission_post(self):
        return True

    def has_permission_put(self):
        return True

    def has_permission_patch(self):
        return True

    def has_permission_options(self):
        return True

    def has_permission_delete(self):
        return True

    def has_permission_create(self):
        return True

    def has_permission_update(self):
        return True

    def has_permission_partial_update(self):
        return True

    def has_permission_list(self):
        return True

    def has_permission_retrieve(self):
        return True

    def has_permission_head(self):
        return True
