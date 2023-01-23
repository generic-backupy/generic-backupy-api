from rest_framework import serializers

from ..models import BackupModule


class BackupModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id', 'name', 'description', 'file_system_path')


class BackupModulePostSerializer(BackupModuleSerializer):
    pass


class BackupModuleRetrieveSerializer(BackupModuleSerializer):
    pass


class BackupModuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id', 'name', 'description')


class BackupModuleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id', 'name')


class BackupOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id',)
