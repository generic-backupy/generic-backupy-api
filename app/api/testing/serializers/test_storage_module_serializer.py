from api.models import StorageModule
from api.serializers.storage_module_serializer import (
    StorageModuleListSerializer, StorageModuleOnlyIdSerializer,
    StorageModuleShortSerializer, StorageModuleRetrieveSerializer)
from django.test import TestCase


class TestStorageModuleSerializer(TestCase):
    def setUp(self):
        self.user = StorageModule.objects.create(
            name = 'test_name',
            description = 'test_description',
        )

    def test_storage_module_serializer(self):
        serializer = StorageModuleRetrieveSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_name', 'description': 'test_description'})
        self.assertNotEqual(serializer.data['name'], 'WRONG_NAME')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')

    def test_storage_module_list_serializer(self):
        serializer = StorageModuleListSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_name', 'description': 'test_description'})
        self.assertNotEqual(serializer.data['name'], 'WRONG_NAME')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')
    
    def test_storage_module_short_serializer(self):
        serializer = StorageModuleShortSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk, 'name': 'test_name'})
        self.assertNotEqual(serializer.data['name'], 'WRONG_NAME')

    def test_storage_module_only_id_serializer(self):
        serializer = StorageModuleOnlyIdSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk})
