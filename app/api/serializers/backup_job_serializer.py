from rest_framework import serializers

from ..models.backup_job import *
from ..serializers.backup_job_storage_module_serializer import *
from ..serializers.secret_serializer import *
from ..serializers.parameter_serializer import *
from ..serializers.storage_module_serializer import *


class BackupJobSerializer(serializers.ModelSerializer):
    secrets = SecretListSerializer(source="backup_module_secrets", many=True)
    parameters = ParameterListSerializer(source="backup_module_parameters", many=True)
    storage_module = StorageModuleListSerializer(source="storage_modules", many=True)

    class Meta:
        model = BackupJob
        fields = ('id', 'name', 'description', 'additional_information',
                  'system', 'backup_module', 'secrets', 'parameters', 'storage_module')


class BackupJobRetrieveSerializer(BackupJobSerializer):
    secrets = SecretRetrieveSerializer(source="backup_module_secrets", many=True)
    parameters = ParameterRetrieveSerializer(source="backup_module_parameters", many=True)
    storage_module = StorageModuleRetrieveSerializer(source="storage_modules", many=True)


class BackupJobPostSerializer(BackupJobSerializer):
    secrets = SecretPostSerializer(source="backup_module_secrets", many=True, required=False)
    parameters = ParameterPostSerializer(source="backup_module_parameters", many=True, required=False)
    storage_module = StorageModulePostSerializer(source="storage_modules", many=True, required=False)

    def create(self, validated_data):
        bj = BackupJob.objects.create(name=validated_data['name'],
                                        description=validated_data['description'],
                                        additional_information=validated_data['additional_information'],
                                        system=validated_data['system'],
                                        backup_module=validated_data['backup_module'])
        if 'secrets' in validated_data.keys():
            bj.backup_module_secrets.set(validated_data['secrets'])
        if 'parameters' in validated_data.keys():
            bj.backup_module_parameters.set(validated_data['parameters'])
        if 'storage_module' in validated_data.keys():
            bj.storage_modules.set(validated_data['storage_module'])
        return bj


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
