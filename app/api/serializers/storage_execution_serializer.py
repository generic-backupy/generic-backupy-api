from api.serializers import BackupJobGetShortSerializer
from rest_framework import serializers

from ..models import StorageExecution


class StorageExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageExecution
        fields = ('id', 'ends_at', 'state',
                  'output', 'logs', 'errors',
                  'backup_job', 'storage_module', 'involved_backup')


class StorageExecutionPostSerializer(StorageExecutionSerializer):
    pass


class StorageExecutionRetrieveSerializer(StorageExecutionSerializer):
    pass


class StorageExecutionListSerializer(serializers.ModelSerializer):
    backup_job = BackupJobGetShortSerializer()

    class Meta:
        model = StorageExecution
        fields = ('id', 'ends_at', 'state', 'backup_job')


class StorageExecutionShortSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('get_info')

    def get_info(self, current_object: StorageExecution):
        if current_object.state == 1:
            return current_object.logs
        if current_object.state == 2:
            return current_object.errors
        if current_object.state == 3:
            return current_object.output

    class Meta:
        model = StorageExecution
        fields = ('id', 'ends_at', 'state', 'info')


class StorageExecutionOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageExecution
        fields = ('id',)
