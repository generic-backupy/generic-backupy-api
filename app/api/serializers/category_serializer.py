from ..models import category
from rest_framework import serializers


class CategoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id', 'name', 'description', 'parent')


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id', 'name', 'description', 'parent')

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id', 'name', 'description')


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id', 'name')


class CategoryOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id',)
