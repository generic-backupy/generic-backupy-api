from rest_framework import serializers

from ..serializers.parameter_serializer import *
from ..serializers.secret_serializer import *
from ..models.backup_job import *


class BackupJobStorageModuleSerializer(serializers.ModelSerializer):
    secret = SecretListSerializer(source="secrets", many=True)
    parameter = ParameterListSerializer(source="parameters", many=True)

    class Meta:
        model = BackupJobStorageModule
        fields = ('id', 'backup_job', 'storage_module', 'secret', 'parameter')


class BackupJobStorageModulePostSerializer(BackupJobStorageModuleSerializer):
    secret = SecretPostSerializer(source="secrets", many=True, required=False)
    parameter = ParameterPostSerializer(source="parameters", many=True, required=False)

    def create(self, validated_data):
        bjsm = BackupJobStorageModule.objects.create(backup_job=validated_data['backup_job'],
                                                     storage_module=validated_data['storage_module'])
        if 'secret' in validated_data.keys():
            bjsm.secrets.add(validated_data['secret'])
        if 'parameter' in validated_data.keys():
            bjsm.parameters.add(validated_data['parameter'])
        return bjsm


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
