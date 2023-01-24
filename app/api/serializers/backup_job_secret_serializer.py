from rest_framework import serializers

from ..models.backup_job import BackupJobSecret
from .secret_serializer import SecretGbModuleSerializer


class BackupJobSecretGbModuleSerializer(serializers.ModelSerializer):
    secret = serializers.SerializerMethodField('get_secret')
    name = serializers.SerializerMethodField('get_name')

    def get_secret(self, current_object: BackupJobSecret):
        return current_object.secret.secret

    def get_name(self, current_object: BackupJobSecret):
        return current_object.secret.name

    class Meta:
        model = BackupJobSecret
        fields = ('id', 'key', 'secret', 'name')


class BackupJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobSecret
        fields = ('id', 'key', 'backup_job', 'secret')


class BackupJobSecretPostSerializer(BackupJobSerializer):
    pass


class BackupJobSecretRetrieveSerializer(BackupJobSerializer):
    pass


class BackupJobSecretBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobSecret
        fields = ('id', 'key')


class BackupJobSecretListSerializer(BackupJobSecretBaseSerializer):
    pass


class BackupJobSecretGetShortSerializer(BackupJobSecretBaseSerializer):
    pass


class BackupJobSecretOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobSecret
        fields = ('id',)
