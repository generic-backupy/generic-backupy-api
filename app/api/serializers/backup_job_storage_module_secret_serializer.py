from rest_framework import serializers

from ..models import BackupJobStorageModuleSecret
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


class BackupJobStorageModuleSecretPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModuleSecret
        fields = ('id', 'key', 'backup_job', 'secret')

class BackupJobStorageModuleSecretRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModuleSecret
        fields = ('id', 'key', 'backup_job', 'secret')

class BackupJobStorageModuleSecretListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BackupJobStorageModuleSecret
        fields = ('id', 'key')

class BackupJobStorageModuleSecretGetShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModuleSecret
        fields = ('id', 'key')

class BackupJobStorageModuleSecretOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobStorageModuleSecret
        fields = ('id',)
