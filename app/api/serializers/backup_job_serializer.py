from rest_framework import serializers

from ..models import BackupJob
from ..serializers.backup_job_secret_serializer import *
from ..serializers.secret_serializer import *


class BackupJobSerializer(serializers.ModelSerializer):
    secrets = serializers.SerializerMethodField('get_list_of_secrets')
    parameters = serializers.SerializerMethodField('get_list_of_parameters')

    def get_list_of_secrets(self, current_object: BackupJob):
        secrets = list(current_object.backup_module_secrets.all())
        ans = []
        for s in secrets:
            ans.append([s.id, s.name])
        return ans

    def get_list_of_parameters(self, current_object: BackupJob):
        params = list(current_object.backup_module_parameters.all())
        ans = []
        for p in params:
            ans.append([p.id, p.name])
        return ans


    class Meta:
        model = BackupJob
        # secrets = BackupJobSecretListSerializer(many=True)
        fields = ('id', 'name', 'description', 'additional_information',
                  'system', 'backup_module', 'storage_modules', 'backup_module_secrets', 'secrets', 'parameters')


class BackupJobRetrieveSerializer(BackupJobSerializer):
    pass


class BackupJobPostSerializer(BackupJobSerializer):
    pass


class BackupJobRetrieveSerializer(BackupJobSerializer):
    pass


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
