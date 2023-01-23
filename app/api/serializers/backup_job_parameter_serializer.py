from rest_framework import serializers

from ..models import BackupJobParameter
from .parameter_serializer import ParameterGbModuleSerializer


class BackupJobParameterGbModuleSerializer(serializers.ModelSerializer):
    parameter = serializers.SerializerMethodField('get_parameter')
    name = serializers.SerializerMethodField('get_name')

    def get_parameter(self, current_object: BackupJobParameter):
        return current_object.parameter.parameter

    def get_name(self, current_object: BackupJobParameter):
        return current_object.parameter.name


    class Meta:
        model = BackupJobParameter
        fields = ('id', 'key', 'parameter', 'name')


class BackupJobParameterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobParameter
        fields = ('id', 'key', 'backup_job', 'parameter')

class BackupJobParameterRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobParameter
        fields = ('id', 'key', 'backup_job', 'parameter')

class BackupJobParameterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BackupJobParameter
        fields = ('id', 'key')

class BackupJobParameterGetShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobParameter
        fields = ('id', 'key')

class BackupJobParameterOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJobParameter
        fields = ('id',)
