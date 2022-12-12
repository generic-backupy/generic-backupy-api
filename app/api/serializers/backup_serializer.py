from ..models import backup
from rest_framework import serializers


class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup
        fields = ('id', 'name', 'description', 'additional_parameters'
                  'backup_job', 'backup_module', 'storage_module',
                  'backup_execution', 'storage_execution')


class BackupPathsSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup
        fields = ('id', 'name', 'path', 'original_file_name')


class BackupShortDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup
        fields = ('id', 'name', 'description', 'additional_parameters')


class BackupShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup
        fields = ('id', 'name')


class BackupOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup
        fields = ('id',)



