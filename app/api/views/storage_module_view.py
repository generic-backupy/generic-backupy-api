import time

from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response

from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import StorageModule, ModuleInstallationExecution
from django.contrib.auth import get_user_model
from ..serializers.storage_module_serializer import *
from api.rq_tasks.module_installation import *

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

    def create(self, request):
        install_execution = ModuleInstallationExecution.objects.create(created_by=request.user)
        try:
            file_uploaded = request.FILES.get('file_uploaded')
            fs = FileSystemStorage(location='/packages')
            filename = fs.save(f"{time.time()}-{file_uploaded.name}", file_uploaded)
            install_module.delay(filename, install_execution, 2)
            return Response()
        except Exception as e:
            install_execution.state = 2
            install_execution.errors = f"error: {e}"
            install_execution.save()
            return Response(f"Error: {e}", 400)

    def get_queryset(self):
        return StorageModule.objects.all()

