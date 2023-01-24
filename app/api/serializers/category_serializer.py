from rest_framework import serializers

from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent')


class CategoryPostSerializer(CategorySerializer):
    pass


class CategoryRetrieveSerializer(CategorySerializer):
    pass


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id',)
