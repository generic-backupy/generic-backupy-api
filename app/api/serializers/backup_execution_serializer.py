from ..models import backup_execution
from rest_framework import serializers


class BackupExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id', 'ends_at', 'state',
                  'output', 'logs', 'errors',
                  'backup_job', 'backup_module')


class BackupExecutionErrorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id,', 'name', 'errors')


class BackupExecutionLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id,', 'name', 'logs')


class BackupExecutionOutputsSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id,', 'name', 'outputs')


class BackupExecutionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id', 'name')


class BackupExecutionOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id',)
