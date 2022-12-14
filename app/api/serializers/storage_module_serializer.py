from ..models import storage_module
from rest_framework import serializers


class StorageModulePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = storage_module
        fields = ('id', 'name', 'description', 'file_system_path')


class StorageModuleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = storage_module
        fields = ('id', 'name', 'description', 'file_system_path')


class StorageModuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = storage_module
        fields = ('id', 'name', 'description')


class StorageModuleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = storage_module
        fields = ('id', 'name')


class StorageModuleOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = storage_module
        fields = ('id',)



