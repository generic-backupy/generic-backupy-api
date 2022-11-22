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
import django_rq
from django_rq import job
from api.rq_tasks.test import *

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
        backup_module = backup_job.backup_module

        # return if no backup_module is specified
        if not backup_module:
            raise AppErrorException("No Backup Module",
                                    "There is no backup module specified for this job", status_code=400)

        # fetch the python module
        python_module = None
        backup_class = None
        # TODO: change the GBModule to the name which is specified in the modules gb.json file.
        # TODO: also replace the python module file name
        module_name = "GBModule"
        module_file = "gb_module.py"
        file_system_path = backup_module.file_system_path
        # append a / if there is no / at the end
        file_system_path += "/" if not file_system_path.endswith("/") else ""
        # get the spec
        spec = importlib.util.spec_from_file_location(module_name, f"{file_system_path}{module_file}")
        if spec:
            python_module = importlib.util.module_from_spec(spec)
            if python_module:
                sys.modules[module_name] = python_module
                spec.loader.exec_module(python_module)
            backup_class = getattr(python_module, module_name)

        if not backup_class:
            raise AppErrorException("BackupModule Loading Error",
                                    "There was an error at the loading process of the backup module", status_code=400)
        module_instance = backup_class()

        do_backup_response = module_instance.do_backup()
        for i in range(6):
            test.delay(i, 2)
        # TODO: What should we do with packages needed by the plugin?
        #   We can't install it locally, because of different versions
        #   Maybe we should execute each package in an own environment or in a docker container?
        #   So each package is a docker image? The communication needs to be over the api, where the container gets a token, to
        #   communicate with the api
        #   Maybe another (more simpler way) is to load the environment of the python module. So each plugin has its own environment
        #   which will be installed, when the user install the plugin. Then we just import the modules of the related environment.
        return Response(f"we got a response :) - {do_backup_response}", 200)


"""
import importlib.util
import sys
module_name = "GBModule"
spec = importlib.util.spec_from_file_location(module_name, f"gb_test_package/gb_module.py")
python_module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = python_module
spec.loader.exec_module(python_module)
"""
