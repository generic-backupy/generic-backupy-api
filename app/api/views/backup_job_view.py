from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .base_view import BaseViewSet
from ..exceptions import MessageStatusCodeException, AppErrorException
from ..rms_base import RmsBaseViewSetFilter
from ..serializers.backup_job_serializer import *
from ..models import BackupJob, Backup
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language as get_language
import os
import importlib.util
import sys
from api.rq_tasks.test import *
from ..utils.backup_util import BackupUtil
from ..utils.package_util import PackageUtil
from django_rq import job
import django_rq

User = get_user_model()



class BackupJobViewSetFilter(RmsBaseViewSetFilter):
    class Meta:
        model = BackupJob
        fields = BackupJob.filterset_fields

class BackupJobViewSet(BaseViewSet):
    serializer_class = BackupJobPostSerializer
    model_class = BackupJob
    filterset_class = BackupJobViewSetFilter

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return BackupJobRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return BackupJobPostSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return BackupJobListSerializer

    def perform_create(self, serializer):
        self.add_user_agent_to_serializer(serializer)
        self.add_field_to_serializer(serializer, "created_by", self.request.user)

        super(BackupJobViewSet, self).perform_create(serializer)

    def get_queryset(self):
        return BackupJob.objects.all()

    @action(detail=True, methods=['get'], url_path='execute/backup',
            permission_classes=(IsAuthenticated,))
    def execute_backup(self, request, *args, **kwargs):
        backup_job = self.get_object()

        BackupUtil.do_backup(backup_job, self.request.user)

        # TODO: What should we do with packages needed by the plugin?
        #   We can't install it locally, because of different versions
        #   Maybe we should execute each package in an own environment or in a docker container?
        #   So each package is a docker image? The communication needs to be over the api, where the container gets a token, to
        #   communicate with the api
        #   Maybe another (more simpler way) is to load the environment of the python module. So each plugin has its own environment
        #   which will be installed, when the user install the plugin. Then we just import the modules of the related environment.
        return Response(f"we got a response :)", 200)


"""
import importlib.util
import sys
module_name = "GBModule"
spec = importlib.util.spec_from_file_location(module_name, f"gb_test_package/gb_module.py")
python_module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = python_module
spec.loader.exec_module(python_module)
"""
