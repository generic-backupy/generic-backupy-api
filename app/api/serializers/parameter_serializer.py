from rest_framework import serializers

from ..models import Parameter


class ParameterGbModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'description', 'parameter')


class ParameterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'description', 'parameter')

class ParameterRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'description', 'parameter')

class ParameterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = ('id', 'name')

class ParameterGetShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name')

class ParameterOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id',)
