from ..models import RestoreExecution
from rest_framework import serializers

from ..serializers import BackupShortSerializer

class RestoreExecutionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestoreExecution
        fields = ('id', 'ends_at', 'state',
                  'output', 'logs', 'errors',
                  'backup_instance')


class RestoreExecutionRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestoreExecution
        fields = ('id', 'ends_at', 'state',
                  'output', 'logs', 'errors',
                  'backup_instance')


class RestoreExecutionListSerializer(serializers.ModelSerializer):
    backup_instance = BackupShortSerializer()
    class Meta:
        model = RestoreExecution
        fields = ('id', 'ends_at', 'state', 'backup_instance')


class RestoreExecutionShortSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('get_info')
    def get_info(self, current_object: RestoreExecution):
        if current_object.state == 0:
            return ""
        if current_object.state == 1:
            return current_object.logs
        if current_object.state == 2:
            return current_object.errors
        if current_object.state == 3:
            return current_object.output
    class Meta:
        model = RestoreExecution
        fields = ('id', 'ends_at', 'state', 'info')


class RestoreExecutionOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestoreExecution
        fields = ('id',)