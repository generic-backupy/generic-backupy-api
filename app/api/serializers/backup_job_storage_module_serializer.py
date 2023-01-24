from rest_framework import serializers

from ..models import BackupJobStorageModule


class BackupJobStorageModuleSerializer(serializers.ModelSerializer):
    secrets = serializers.SerializerMethodField('get_list_of_secrets')
    parameters = serializers.SerializerMethodField('get_list_of_parameters')

    def get_list_of_secrets(self, current_object: BackupJobStorageModule):
        secrets = list(current_object.secrets.all())
        ans = []
        for s in secrets:
            ans.append([s.id, s.name])
        return ans

    def get_list_of_parameters(self, current_object: BackupJobStorageModule):
        params = list(current_object.parameters.all())
        ans = []
        for p in params:
            ans.append([p.id, p.name])

        return ans

    class Meta:
        model = BackupJobStorageModule
        fields = ('id', 'backup_job', 'storage_module', 'secrets', 'parameters')


class BackupJobStorageModulePostSerializer(BackupJobStorageModuleSerializer):
    pass


class BackupJobStorageModuleRetrieveSerializer(BackupJobStorageModuleSerializer):
    pass


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
