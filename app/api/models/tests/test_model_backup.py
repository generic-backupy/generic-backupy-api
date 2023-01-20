from django.test import TestCase

from api.models import Backup
from django.db import IntegrityError


# Create your tests here.
class TestModelBackup(TestCase):

    def setUp(self):
        backups = Backup.objects.all()
        backups.delete()

    def test_empty_required_fields(self):
        with self.assertRaises(IntegrityError):
            b = Backup.objects.create(name=None)

    def test_create_required_fields_only(self):
        b = Backup.objects.create(name="name")
        backups = Backup.objects.all()
        self.assertEqual(len(backups), 1, "Object not added to db")
        self.assertIsInstance(backups[0].id, int, "Object has wrong autogenerated id")
        self.assertEqual(backups[0].name, "name", "Object has wrong name, failed to save properly")
        self.assertIsNone(backups[0].original_file_name, "Default value for not required field is not empty")

    def test_create_more_fields(self):
        b = Backup.objects.create(name="name", original_file_name="file", path="path")
        backups = Backup.objects.all()
        self.assertEqual(len(backups), 1, "Object not added to db")
        self.assertIsInstance(backups[0].id, int, "Object has wrong autogenerated id")
        self.assertEqual(backups[0].name, "name", "Object has wrong name, failed to save properly")
        self.assertEqual(backups[0].original_file_name, "file",
                         "Object has wrong content in field 'original_file_name'")
        self.assertEqual(backups[0].path, "path", "Object has wrong content in field 'path'")
        self.assertIsNone(backups[0].description, "Default value for not required field is not empty")

    def test_delete(self):
        b = Backup.objects.create(name="name")
        backups = Backup.objects.all()
        backups.delete()
        self.assertEqual(len(backups), 0, "Error while deleting")