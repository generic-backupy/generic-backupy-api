from rest_framework import serializers

from ..models import BackupJobStorageModule

class BackupJobStorageModulePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModule
        fields = ('id', 'backup_job', 'storage_module')

class BackupJobStorageModuleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModule
        fields = ('id', 'backup_job', 'storage_module')

class BackupJobStorageModuleListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    def get_name(self, current_object: BackupJobStorageModule):
        return current_object.backup_job.name
    class Meta:
        model = BackupJobStorageModule
        fields = ('id', 'name')

class BackupJobStorageModuleGetShortSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, current_object: BackupJobStorageModule):
        return current_object.backup_job.name
    class Meta:
        model = BackupJobStorageModule
        fields = ('id', 'name')

class BackupJobStorageModuleOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModule
        fields = ('id',)
