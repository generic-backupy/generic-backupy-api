from django.test import TestCase
from api.models import BackupModule
from django.db import IntegrityError


class TestModelBackup(TestCase):

    def setUp(self):
        db = BackupModule.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            BackupModule.objects.create(name=None)

    def test_create_required_fields_only(self):
        BackupModule.objects.create(name="name")
        db = BackupModule.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertIsNone(db[0].description, "Wrong default value in 'description'")

    def test_create_all_fields(self):
        BackupModule.objects.create(name="name", description="desc")
        db = BackupModule.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].description, "desc", "Error in field 'description'")

    def test_delete(self):
        BackupModule.objects.create(name="name")
        db = BackupModule.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")
