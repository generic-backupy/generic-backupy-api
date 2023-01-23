from rest_framework import serializers

from ..models import BackupJobStorageModuleParameter
from .parameter_serializer import ParameterGbModuleSerializer


class BackupJobStorageModuleParameterGbModuleSerializer(serializers.ModelSerializer):
    parameter = serializers.SerializerMethodField('get_parameter')
    name = serializers.SerializerMethodField('get_name')
    id = serializers.SerializerMethodField('get_id')

    def get_parameter(self, current_object: BackupJobStorageModuleParameter):
        return current_object.parameter.parameter

    def get_name(self, current_object: BackupJobStorageModuleParameter):
        return current_object.parameter.name

    def get_id(self, current_object: BackupJobStorageModuleParameter):
        return current_object.parameter.id

    class Meta:
        model = BackupJobStorageModuleParameter
        fields = ('id', 'key', 'secret', 'name')


class BackupJobStorageModuleParameterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModuleParameter
        fields = ('id', 'key', 'backup_job_storage_module', 'parameter')

class BackupJobStorageModuleParameterRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModuleParameter
        fields = ('id', 'key', 'backup_job_storage_module', 'parameter')

class BackupJobStorageModuleParameterListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    def get_name(self, current_object: BackupJobStorageModuleParameter):
        return current_object.backup_job_storage_module.name
    class Meta:
        model = BackupJobStorageModuleParameter
        fields = ('id', 'name')

class BackupJobStorageModuleParameterGetShortSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, current_object: BackupJobStorageModuleParameter):
        return current_object.backup_job_storage_module.name

    class Meta:
        model = BackupJobStorageModuleParameter
        fields = ('id', 'name')

class BackupJobStorageModuleParameterOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModuleParameter
        fields = ('id',)
