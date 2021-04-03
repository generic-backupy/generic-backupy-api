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
        return Response()
