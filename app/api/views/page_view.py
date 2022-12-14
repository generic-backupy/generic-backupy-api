from api.models import BackupExecution, StorageExecution, Backup, System, BackupJob
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .base_view import BaseViewSet
from rest_framework.response import Response



class PageViewSet(BaseViewSet):
    serializer_class = None
    http_method_names = ['get', ]

    @action(detail=False, methods=['get'], url_path='home')
    def home(self, request, *args, **kwargs):
        page_json = {}
        page_json["latest-backup-jobs"] = BackupExecution.objects.all()[:5]
        page_json["latest-storage-jobs"] = StorageExecution.objects.all()[:5]
        page_json["latest-backups"] = Backup.objects.all()[:5]
        page_json["systems"] = System.objects.all()[:5]
        page_json["backup-jobs"] = BackupJob.objects.all()[:5]
        return Response(page_json)
