from rest_framework import serializers

from ..models.backup_job import BackupJobStorageModuleSecret
from .secret_serializer import SecretGbModuleSerializer


class BackupJobStorageModuleSecretGbModuleSerializer(serializers.ModelSerializer):
    secret = serializers.SerializerMethodField('get_secret')
    name = serializers.SerializerMethodField('get_name')
    id = serializers.SerializerMethodField('get_id')

    def get_secret(self, current_object: BackupJobStorageModuleSecret):
        return current_object.secret.secret

    def get_name(self, current_object: BackupJobStorageModuleSecret):
        return current_object.secret.name

    def get_id(self, current_object: BackupJobStorageModuleSecret):
        return current_object.secret.id

    class Meta:
        model = BackupJobStorageModuleSecret
        fields = ('id', 'key', 'secret', 'name')


class BackupJobStorageModuleSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModuleSecret
        fields = ('id', 'key', 'backup_job', 'secret')


class BackupJobStorageModuleSecretPostSerializer(BackupJobStorageModuleSecretSerializer):
    pass


class BackupJobStorageModuleSecretRetrieveSerializer(BackupJobStorageModuleSecretSerializer):
    pass


class BackupJobStorageModuleSecretBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = BackupJobStorageModuleSecret
        fields = ('id', 'key')


class BackupJobStorageModuleSecretListSerializer(BackupJobStorageModuleSecretBaseSerializer):
    pass


class BackupJobStorageModuleSecretGetShortSerializer(BackupJobStorageModuleSecretBaseSerializer):
    pass


class BackupJobStorageModuleSecretOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModuleSecret
        fields = ('id',)
