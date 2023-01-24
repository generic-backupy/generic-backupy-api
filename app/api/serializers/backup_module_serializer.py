from rest_framework import serializers
from ..models import BackupModule


class BackupModulePostSerializer(serializers.ModelSerializer):
    file_uploaded = serializers.FileField()
    class Meta:
        model = BackupModule
        fields = ('file_uploaded',)


class BackupModuleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id', 'name', 'description')


class BackupModuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id', 'name', 'description')


class BackupModuleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id', 'name')


class BackupOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupModule
        fields = ('id',)
