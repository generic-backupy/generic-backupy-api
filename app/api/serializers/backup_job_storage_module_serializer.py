from rest_framework import serializers

from ..serializers.parameter_serializer import *
from ..serializers.secret_serializer import *
from ..models import BackupJobStorageModule


class BackupJobStorageModuleSerializer(serializers.ModelSerializer):
    secret = SecretListSerializer(source="secrets", many=True)
    parameter = ParameterListSerializer(source="parameters", many=True)

    class Meta:
        model = BackupJobStorageModule
        fields = ('id', 'backup_job', 'storage_module', 'secret', 'parameter')


class BackupJobStorageModulePostSerializer(BackupJobStorageModuleSerializer):
    secret = SecretPostSerializer(source="secrets", many=True, required=False)
    parameter = ParameterPostSerializer(source="parameters", many=True, required=False)


class BackupJobStorageModuleRetrieveSerializer(BackupJobStorageModuleSerializer):
    secret = SecretRetrieveSerializer(source="secrets", many=True)
    parameter = ParameterRetrieveSerializer(source="parameters", many=True)


class BackupJobStorageModuleBaseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, current_object: BackupJobStorageModule):
        return current_object.backup_job.name

    class Meta:
        model = BackupJobStorageModule
        fields = ('id', 'name')


class BackupJobStorageModuleListSerializer(BackupJobStorageModuleBaseSerializer):
    pass


class BackupJobStorageModuleGetShortSerializer(BackupJobStorageModuleBaseSerializer):
    pass


class BackupJobStorageModuleOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModule
        fields = ('id',)
