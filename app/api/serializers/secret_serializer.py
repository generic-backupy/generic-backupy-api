from rest_framework import serializers

from ..models import Secret


class SecretGbModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ('id', 'name', 'description', 'secret')


class SecretPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ('id', 'name', 'description', 'secret')

class SecretRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ('id', 'name', 'description', 'secret')

class SecretListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Secret
        fields = ('id', 'name')

class SecretGetShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ('id', 'name')

class SecretOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ('id',)
