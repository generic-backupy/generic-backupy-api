from rest_framework import serializers

from ..models import PushToken

class PushTokenPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = ('key',)


class PushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        exclude = ('created_with_user_agent',)


class PushTokenRetrieveSerializer(PushTokenSerializer):
    pass

class PushTokenListSerializer(PushTokenSerializer):
    pass


class PushTokenGetShortSerializer(PushTokenSerializer):
    pass


class PushTokenOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = ('id',)
