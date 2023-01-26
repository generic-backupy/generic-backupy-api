from api.models import Backup
from api.serializers.backup_serializer import (
    BackupListSerializer, BackupOnlyIdSerializer, BackupPathsSerializer,
    BackupPostSerializer, BackupRetrieveSerializer, BackupSerializer,
    BackupShortDescriptionSerializer, BackupShortSerializer)
from django.test import TestCase


class TestBackupSerializer(TestCase):
    def setUp(self):
        self.user = Backup.objects.create(
            name = 'test_',
            description = 'test_description',
            additional_parameters = {'a':1,'b':2},
            path = '../test_path',
            original_file_name = 'test_original_file_name',
        )

    def test_backup_serializer(self):
        serializer = BackupSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertEqual(serializer.data['additional_parameters'], {'a':1,'b':2})
        self.assertNotEqual(serializer.data['additional_parameters'], {'a':1,'c':2})
        self.assertEqual(serializer.data['path'], '../test_path')
        self.assertNotEqual(serializer.data['path'], '../wrong_path')
        self.assertEqual(serializer.data['original_file_name'], 'test_original_file_name')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')
        self.assertEqual(serializer.data['id'],  self.user.pk)


    def test_backup_id_only_serializer(self):
        serializer = BackupOnlyIdSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk})

    def test_backup_short_description_serializer(self):
        serializer = BackupShortDescriptionSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_', 'description': 'test_description', 
                         'additional_parameters': {'a':1,'b':2}})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['additional_parameters'], {'a':1,'c':2})
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')

    def test_backup_short_serializer(self):
        serializer = BackupShortSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')

    def test_backup_paths_serializer(self):
        serializer = BackupPathsSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_', 'path': '../test_path', 'original_file_name': 'test_original_file_name'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['path'], '../wrong_path')
        self.assertNotEqual(serializer.data['original_file_name'], 'wrong_file_name')

    def test_backup_post_serializer(self):
        serializer = BackupPostSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertEqual(serializer.data['additional_parameters'], {'a':1,'b':2})
        self.assertNotEqual(serializer.data['additional_parameters'], {'a':1,'c':2})
        self.assertEqual(serializer.data['path'], '../test_path')
        self.assertNotEqual(serializer.data['path'], '../wrong_path')
        self.assertEqual(serializer.data['original_file_name'], 'test_original_file_name')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')
        self.assertEqual(serializer.data['id'],  self.user.pk)

    def test_backup_retrieve_serializer(self):
        serializer = BackupRetrieveSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertEqual(serializer.data['additional_parameters'], {'a':1,'b':2})
        self.assertNotEqual(serializer.data['additional_parameters'], {'a':1,'c':2})
        self.assertEqual(serializer.data['path'], '../test_path')
        self.assertNotEqual(serializer.data['path'], '../wrong_path')
        self.assertEqual(serializer.data['original_file_name'], 'test_original_file_name')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')
        self.assertEqual(serializer.data['id'],  self.user.pk)

    def test_backup_list_serializer(self):
        serializer = BackupListSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertEqual(serializer.data['path'], '../test_path')
        self.assertNotEqual(serializer.data['path'], '../wrong_path')
        self.assertEqual(serializer.data['original_file_name'], 'test_original_file_name')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')
        self.assertEqual(serializer.data['id'],  self.user.pk)

