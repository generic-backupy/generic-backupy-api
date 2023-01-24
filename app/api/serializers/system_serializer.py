from rest_framework import serializers

from ..models import System


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id', 'name', 'description', 'host',
                  'additional_information', 'category')


class SystemPostSerializer(SystemSerializer):
    pass


class SystemRetrieveSerializer(SystemSerializer):
    pass


class SystemGbModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id', 'name', 'description',
                  'host', 'additional_information')


class SystemBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id', 'name')


class SystemListSerializer(SystemBaseSerializer):
    pass


class SystemGetShortSerializer(SystemBaseSerializer):
    pass


class SystemOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id',)
