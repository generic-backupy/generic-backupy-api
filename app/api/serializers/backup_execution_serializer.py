from ..models import BackupExecution
from rest_framework import serializers
from .backup_job_serializer import BackupJobGetShortSerializer


class BackupExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupExecution
        fields = ('id', 'ends_at', 'state',
                  'output', 'logs', 'errors',
                  'backup_job', 'backup_module')


class BackupExecutionPostSerializer(BackupExecutionSerializer):
    pass


class BackupExecutionRetrieveSerializer(BackupExecutionSerializer):
    pass


class BackupExecutionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupExecution
        fields = ('id,', 'state', 'errors')


class BackupExecutionErrorsSerializer(BackupExecutionBaseSerializer):
    pass


class BackupExecutionLogsSerializer(BackupExecutionBaseSerializer):
    pass


class BackupExecutionOutputsSerializer(BackupExecutionBaseSerializer):
    pass


class BackupExecutionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupExecution
        fields = ('id', 'state')


class BackupExecutionOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupExecution
        fields = ('id',)


class BackupExecutionListSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('get_info')
    backup_job = BackupJobGetShortSerializer()

    def get_info(self, current_object: BackupExecution):
        if current_object.state == 1:
            return current_object.logs
        if current_object.state == 2:
            return current_object.errors
        if current_object.state == 3:
            return current_object.output

    class Meta:
        model = BackupExecution
        fields = ('id', 'ends_at', 'state', 'info', 'backup_job')
