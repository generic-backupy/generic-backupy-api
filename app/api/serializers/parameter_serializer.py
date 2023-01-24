from rest_framework import serializers

from ..models.parameter import Parameter


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'description', 'parameter')


class ParameterGbModuleSerializer(ParameterSerializer):
    pass


class ParameterPostSerializer(ParameterSerializer):
    pass


class ParameterRetrieveSerializer(ParameterSerializer):
    pass


class ParameterBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name')


class ParameterListSerializer(ParameterBaseSerializer):
    pass


class ParameterGetShortSerializer(ParameterBaseSerializer):
    pass


class ParameterOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id',)
