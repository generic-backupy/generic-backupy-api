from rest_framework import serializers

from ..models import BackupJob


class BackupJobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJob
        fields = ('id', 'name', 'description', 'additional_information',
                  'system', 'backup_module', 'storage_modules')

class BackupJobRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJob
        fields = ('id', 'name', 'description', 'additional_information',
                  'system', 'backup_module', 'storage_modules')

class BackupJobListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BackupJob
        fields = ('id', 'name')

class BackupJobGetShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJob
        fields = ('id', 'name')

class BackupJobOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJob
        fields = ('id',)
