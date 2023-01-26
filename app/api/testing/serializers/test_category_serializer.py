from api.models import Category
from api.serializers.category_serializer import (CategoryListSerializer,
                                                 CategoryOnlyIdSerializer,
                                                 CategoryPostSerializer,
                                                 CategoryRetrieveSerializer,
                                                 CategorySerializer,
                                                 CategoryShortSerializer)

from django.test import TestCase


class TestCategorySerializer(TestCase):
    def setUp(self):
        self.user = Category.objects.create(
            name = 'test_',
            description = 'test_description',
        )

    def test_category_serializer(self):
        serializer = CategorySerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertEqual(serializer.data['id'],  self.user.pk)
    
    def test_category_id_only_serializer(self):
        serializer = CategoryOnlyIdSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk})


    def test_category_short_serializer(self):
        serializer = CategoryShortSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk, 'name': 'test_'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')

    def test_category_post_serializer(self):
        serializer = CategoryPostSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertEqual(serializer.data['id'],  self.user.pk)

    def test_category_retrieve_serializer(self):
        serializer = CategoryRetrieveSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertEqual(serializer.data['id'],  self.user.pk)

    def test_category_list_serializer(self):
        serializer = CategoryListSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertEqual(serializer.data['id'],  self.user.pk)

