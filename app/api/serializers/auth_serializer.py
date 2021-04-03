from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    push_token = serializers.CharField(write_only=True, required=False)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            user.push_token = data.get('push_token')
            return user
        raise serializers.ValidationError('Incorrect Credentials')
