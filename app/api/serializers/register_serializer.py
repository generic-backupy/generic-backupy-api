from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from knox.models import AuthToken

from api.models import PushToken
from api.utils.email_util import EmailUtil
from django.conf import settings

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    token = serializers.CharField(read_only=True)
    push_token = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'token', 'push_token')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            created_with_user_agent=validated_data['created_with_user_agent'],
            created_language=validated_data['created_language']
        )
        now = timezone.now()
        user.set_password(validated_data['password'])
        user.last_privacy_check = now
        user.last_conditions_check = now

        user.privacy_version = settings.PRIVACY_VERSION
        user.conditions_version = settings.CONDITIONS_VERSION

        user.save()
        user.add_package(UserPackages.PREMIUM, extend_with_days=30 * 3)

        auth_token = AuthToken.objects.create(user)

        user.token = auth_token[1]
        push_token = validated_data.get('push_token')
        if push_token:
            token = PushToken(auth_token=auth_token[0], key=push_token)
            token.save()

        try:
            EmailUtil.send_verification_code(user)
        except Exception as e:
            print("Email Error")

        return user
