from rest_framework import serializers

from ..models import System


class SystemGbModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id', 'name', 'description', 'host', 'additional_information')


class SystemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id', 'name', 'description', 'host', 'additional_information', 'category')

class SystemRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id', 'name', 'description', 'host', 'additional_information', 'category')

class SystemListSerializer(serializers.ModelSerializer):

    class Meta:
        model = System
        fields = ('id', 'name')

class SystemGetShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id', 'name')

class SystemOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id',)
