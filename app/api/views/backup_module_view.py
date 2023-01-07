from django.core.files.storage import FileSystemStorage

from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetFilter
from ..models import BackupModule, ModuleInstallationExecution
from django.contrib.auth import get_user_model
import time

from ..rq_tasks.module_installation import install_module
from ..serializers.backup_module_serializer import *
from rest_framework.response import Response

User = get_user_model()


class BackupModuleViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = BackupModule
        fields = BackupModule.filterset_fields

class BackupModuleViewSet(BaseViewSet):
    serializer_class = BackupModulePostSerializer
    model_class = BackupModule
    filterset_class = BackupModuleViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return BackupModuleRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return BackupModulePostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return BackupModuleListSerializer


    def create(self, request):
        install_execution = ModuleInstallationExecution.objects.create(created_by=request.user)
        try:
            file_uploaded = request.FILES.get('file_uploaded')
            content_type = file_uploaded.content_type
            fs = FileSystemStorage(location='/packages')
            filename = fs.save(f"{time.time()}-{file_uploaded.name}", file_uploaded)
            response = "POST API and you have uploaded a {} file".format(content_type)
            install_module.delay(filename, install_execution)
            return Response(response)
        except Exception as e:
            install_execution.state = 2
            install_execution.errors = f"error: {e}"
            install_execution.save()
            return Response(f"Error: {e}", 400)

    def get_queryset(self):
        return BackupModule.objects.all()

