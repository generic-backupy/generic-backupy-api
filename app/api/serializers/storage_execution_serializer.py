from ..models import storage_execution
from rest_framework import serializers


class StorageExecutionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = storage_execution
        fields = ('id', 'ends_at', 'state',
                  'output', 'logs', 'errors',
                  'backup_job', 'storage_module', 'involved_backup')


class StorageExecutionRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = storage_execution
        fields = ('id', 'ends_at', 'state',
                  'output', 'logs', 'errors',
                  'backup_job', 'storage_module', 'involved_backup')


class StorageExecutionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = storage_execution
        fields = ('id', 'ends_at', 'state')


class StorageExecutionShortSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('get_info')
    def get_info(self, current_object: storage_execution):
        if current_object.state == 1:
            return current_object.logs
        if current_object.state == 2:
            return current_object.errors
        if current_object.state == 3:
            return current_object.output
    class Meta:
        model = storage_execution
        fields = ('id', 'ends_at', 'state', 'info')


class StorageExecutionOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = storage_execution
        fields = ('id',)



