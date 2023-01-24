from rest_framework import serializers

from ..models import StorageModule

class StorageModulePostSerializer(serializers.ModelSerializer):
    file_uploaded = serializers.FileField()
    class Meta:
        model = StorageModule
        fields = ('file_uploaded',)


class StorageModuleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageModule
        fields = ('id', 'name', 'description')


class StorageModuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageModule
        fields = ('id', 'name', 'description')


class StorageModuleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageModule
        fields = ('id', 'name')


class StorageModuleOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageModule
        fields = ('id',)
