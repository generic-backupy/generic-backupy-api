from ..models import backup_execution
from rest_framework import serializers


class BackupPostExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id', 'ends_at', 'state',
                  'output', 'logs', 'errors',
                  'backup_job', 'backup_module')


class BackupRetrieveExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id', 'ends_at', 'state',
                  'output', 'logs', 'errors',
                  'backup_job', 'backup_module')


class BackupExecutionErrorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id,', 'state', 'errors')


class BackupExecutionLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id,', 'state', 'logs')


class BackupExecutionOutputsSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id,', 'state', 'outputs')


class BackupExecutionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id', 'state')


class BackupExecutionOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = backup_execution
        fields = ('id',)


class BackupExecutionListSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('get_info')
    def get_info(self, current_object: backup_execution):
        if current_object.state == 1:
            return current_object.logs
        if current_object.state == 2:
            return current_object.errors
        if current_object.state == 3:
            return current_object.output
    class Meta:
        model = backup_execution
        fields = ('id', 'ends_at', 'state', 'info')
