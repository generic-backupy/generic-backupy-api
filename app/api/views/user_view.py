from datetime import timedelta

from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from knox import crypto

from .base_view import BaseViewSet
from ..rms_base import RmsBaseViewSetPermission
from ..serializers import *
from django.contrib.auth import get_user_model
from ..exceptions import MessageStatusCodeException, AppErrorException
from ..utils.email_util import EmailUtil
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = get_user_model()
from django.utils.timezone import datetime, timezone

from rest_framework.permissions import IsAuthenticated

class UserViewSet(BaseViewSet):
    serializer_class = UserPostSerializer
    http_method_names = ['get', 'put', 'patch', 'options', 'delete', ]
    model_class = User

    def has_permission_post(self):
        return False

    def get_serializer_retrieve_class(self, *args, **kwargs):
        return UserRetrieveSerializer

    def get_serializer_create_class(self, *args, **kwargs):
        return UserPostSerializer

    def get_serializer_partial_update_class(self, *args, **kwargs):
        return UserUpdateSerializer

    def get_serializer_update_class(self, *args, **kwargs):
        return UserUpdateSerializer

    def get_serializer_list_class(self, *args, **kwargs):
        return UserListSerializer

    def perform_update(self, serializer):
        # check if the email needs an update
        if serializer.validated_data.get('email'):
            super(UserViewSet, self).perform_update(serializer)
            self.request.user.email = serializer.validated_data.get('email')
            self.request.user.email_verified = False
            self.request.user.save()
            self.send_verification_code()
        else:
            super(UserViewSet, self).perform_update(serializer)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user

        # delete user
        try:
            user.delete()
        except ProtectedError as e:
            raise MessageStatusCodeException(e, status_code=status.HTTP_423_LOCKED)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='own')
    def own(self, request, *args, **kwargs):
        serializer = UserRetrieveSerializer(self.request.user)

        return Response(serializer.data)

    def send_verification_code(self):
        return EmailUtil.send_verification_code(self.request.user)

    @action(detail=False, methods=['get'], url_path='verification-code', permission_classes=(IsAuthenticated,), should_use_additional_permission_classes=False)
    def verification_code(self, request, *args, **kwargs):
        code = self.send_verification_code()
        return Response()

    @action(detail=False, methods=['get'], url_path='logout', permission_classes=(IsAuthenticated,))
    def logout(self, request, *args, **kwargs):
        token_header = request.META.get('HTTP_AUTHORIZATION')
        token = token_header.replace("Token ", "")
        digest = crypto.hash_token(token)
        token = AuthToken.objects.filter(digest=digest).first()
        if token:
            token.delete()
            return Response()
        return Response(status=404)

    @action(detail=False, methods=['get'], url_path='verify/(?P<code>.+)', permission_classes=None)
    def verify(self, request, *args, **kwargs):
        code = kwargs['code']

        user: User = User.objects.filter(email_verification_code=code,
                                         email_verification_code_created_at__gte=
                                   datetime.now(timezone.utc)-timedelta(days=1))\
            .first()

        if user:
            user.email_verified = True
            user.email_verification_code_accepted_at = datetime.now(timezone.utc)
            user.save()
            return Response()

        return Response(status=404)

    @action(detail=False, methods=['get'], url_path='accept-privacy')
    def accept_privacy(self, request, *args, **kwargs):
        user = request.user

        user.privacy_version = settings.PRIVACY_VERSION
        user.last_privacy_check = datetime.now()
        user.save()

        return Response(status=200)

    @action(detail=False, methods=['get'], url_path='accept-conditions')
    def accept_conditions(self, request, *args, **kwargs):
        user = request.user

        user.conditions_version = settings.CONDITIONS_VERSION
        user.last_conditions_check = datetime.now()
        user.save()

        return Response(status=200)
