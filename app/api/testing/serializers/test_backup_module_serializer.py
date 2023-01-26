from api.models import BackupModule
from api.serializers.backup_module_serializer import (
    BackupModuleListSerializer, BackupModulePostSerializer,
    BackupModuleRetrieveSerializer, BackupModuleShortSerializer,
    BackupOnlyIdSerializer)
from django.test import TestCase


class TestBackupModuleSerializer(TestCase):
    def setUp(self):
        self.user = BackupModule.objects.create(
            name = 'test_',
            description = 'test_description',
            module_config = {'a':1,'b':2},
            file_system_path = '../test_path',
        )

    def test_backup_module_retrieve_serializer(self):
        serializer = BackupModuleRetrieveSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_', 'description': 'test_description'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')

    def test_backup_module_list_serializer(self):
        serializer = BackupModuleListSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_', 'description': 'test_description'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')

    def test_backup_module_short_serializer(self):
        serializer = BackupModuleShortSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')

    def test_backup_module_id_only_serializer(self):
        serializer = BackupOnlyIdSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk})

