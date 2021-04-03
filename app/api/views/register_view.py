import secrets

from django.template.loader import render_to_string

from ..exceptions import AppErrorException
from ..models import PasswordResetToken
from ..serializers import RegisterSerializer, ChangePasswordSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from ..utils.email_util import EmailUtil

User = get_user_model()
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string
from django.utils.timezone import datetime, timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language as get_language


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer._validated_data["created_with_user_agent"] = self.request.META['HTTP_USER_AGENT']
        serializer._validated_data["created_language"] = get_language()
        super(RegisterView, self).perform_create(serializer)

class UsernameAvailableView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        username = self.request.query_params.get('username', None)

        if username:
            return Response(not User.objects.filter(username=username).exists())

        return Response(None, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        email = self.request.query_params.get('email', None)

        if email:
            user = User.objects.filter(email=email).first()
            if user and user.email_verified:
                # check if a request code was requested in the last minute
                if user.reset_password_code_last_request and (datetime.now(timezone.utc) - user.reset_password_code_last_request).seconds < 1*60:
                    raise AppErrorException(_("too-many-requests"), _("password.reset.too_many_requests"), status_code=429)

                token = PasswordResetToken(token=get_random_string(length=12), user=user)
                PasswordResetToken.objects.filter(user=user).delete()
                token.save()

                user.reset_password_code_last_request = datetime.now(timezone.utc)
                user.save()

                # send email
                css_part = render_to_string("email/styles.html")
                html_template = render_to_string("email/forgot-password.html", {
                    'token': token.token,
                    'css_part': css_part
                })
                EmailUtil.send_to_user("Reset Password", "B", user,
                                       html_message=html_template)


            return Response(None, status=status.HTTP_204_NO_CONTENT)

        return Response(None, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (AllowAny,)

    http_method_names = ["post"]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = PasswordResetToken.objects.filter(token=serializer.validated_data['token']).first()
            if token and token.created_at and (datetime.now(timezone.utc) - token.created_at).days < 2:
                token.user.set_password(serializer.validated_data['password'])
                token.user.save()
                token.delete()
                return Response(None, status=status.HTTP_201_CREATED)

            return Response('invalid token', status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailAvailableView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        email = self.request.query_params.get('email', None)

        if email:
            return Response(not User.objects.filter(email=email).exists())

        return Response(None, status=status.HTTP_400_BAD_REQUEST)
