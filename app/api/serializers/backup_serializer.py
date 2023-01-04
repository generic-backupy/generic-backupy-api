from ..models import Backup
from rest_framework import serializers


class BackupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ('id', 'name', 'description', 'additional_parameters',
                  'path', 'original_file_name',
                  'backup_job', 'backup_module', 'backup_job_storage_module',
                  'backup_execution', 'storage_execution')


class BackupRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ('id', 'name', 'description', 'additional_parameters',
                  'path', 'original_file_name',
                  'backup_job', 'backup_module', 'backup_job_storage_module',
                  'backup_execution', 'storage_execution')


class BackupPathsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ('id', 'name', 'path', 'original_file_name')


class BackupShortDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ('id', 'name', 'description', 'additional_parameters')


class BackupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ('id', 'name', 'description', 'path', 'original_file_name', 'created_at')


class BackupShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ('id', 'name')


class BackupOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ('id',)



