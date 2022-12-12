from ..models import category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id', 'name', 'description', 'parent')


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id', 'name')


class CategoryOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id',)
