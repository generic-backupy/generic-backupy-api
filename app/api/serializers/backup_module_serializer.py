from ..models import BackupModule
from rest_framework import serializers

class BackupModulePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id', 'name', 'description', 'file_system_path')


class BackupModuleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id', 'name', 'description', 'file_system_path')


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
