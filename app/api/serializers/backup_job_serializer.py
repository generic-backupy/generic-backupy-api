from rest_framework import serializers

from ..models import BackupJob


class BackupJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJob
        fields = ('id', 'name', 'description', 'additional_information',
                  'system', 'backup_module', 'storage_modules')


class BackupJobRetrieveSerializer(BackupJobSerializer):
    pass


class BackupJobPostSerializer(BackupJobSerializer):
    pass


class BackupJobRetrieveSerializer(BackupJobSerializer):
    pass


class BackupJobBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJob
        fields = ('id', 'name')


class BackupJobListSerializer(BackupJobBaseSerializer):
    pass


class BackupJobGetShortSerializer(BackupJobBaseSerializer):
    pass


class BackupJobOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJob
        fields = ('id',)
