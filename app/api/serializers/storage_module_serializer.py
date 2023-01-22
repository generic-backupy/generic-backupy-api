from rest_framework import serializers

from ..models import StorageModule


class StorageModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageModule
        fields = ('id', 'name', 'description', 'file_system_path')


class StorageModulePostSerializer(StorageModuleSerializer):
    pass


class StorageModuleRetrieveSerializer(StorageModuleSerializer):
    pass


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
