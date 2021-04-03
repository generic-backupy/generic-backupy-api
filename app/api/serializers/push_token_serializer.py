from rest_framework import serializers

from ..models import PushToken

class PushTokenRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        exclude = ('created_with_user_agent',)

class PushTokenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        exclude = ('created_with_user_agent',)

class PushTokenPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = ('key',)

class PushTokenGetShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        exclude = ('created_with_user_agent',)

class PushTokenOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = ('id',)
