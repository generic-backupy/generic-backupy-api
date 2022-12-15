from api.serializers.category_serializer import CategoryListSerializer

from api.models import BackupExecution, StorageExecution, Backup, System, BackupJob, Category
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .base_view import BaseViewSet
from rest_framework.response import Response
from ..serializers.backup_execution_serializer import BackupExecutionListSerializer
from ..serializers.storage_execution_serializer import StorageExecutionListSerializer
from ..serializers.backup_job_serializer import BackupJobListSerializer
from ..serializers.system_serializer import SystemListSerializer

class PageViewSet(BaseViewSet):
    serializer_class = None
    http_method_names = ['get', ]

    @action(detail=False, methods=['get'], url_path='home')
    def home(self, request, *args, **kwargs):
        page_json = {}
        page_json["backup_jobs"] = BackupJobListSerializer(BackupJob.objects.all()[:15], many=True).data
        page_json["systems"] = SystemListSerializer(System.objects.all()[:15], many=True).data
        page_json["categories"] = CategoryListSerializer(Category.objects.all()[:15], many=True).data
        page_json["latest_backup_executions"] = BackupExecutionListSerializer(BackupExecution.objects.all().order_by('-id')[:15], many=True).data
        page_json["latest_storage_executions"] = StorageExecutionListSerializer(StorageExecution.objects.all().order_by('-id')[:15], many=True).data
        return Response(page_json)
