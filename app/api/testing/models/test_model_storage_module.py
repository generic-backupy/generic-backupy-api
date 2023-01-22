from django.db import IntegrityError
from django.test import TestCase

from api.models import StorageModule


class TestModelStorageModule(TestCase):

    def setUp(self):
        db = StorageModule.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            StorageModule.objects.create(name=None)

    def test_create_required_fields_only(self):
        StorageModule.objects.create(name="name")
        db = StorageModule.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertIsNone(db[0].description, "Wrong default value in 'description'")

    def test_create_all_fields(self):
        StorageModule.objects.create(name="name", description="desc", file_system_path="path")
        db = StorageModule.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].description, "desc", "Error in field 'description'")
        self.assertEqual(db[0].file_system_path, "path", "Error in field 'file_system_path'")

    def test_delete(self):
        StorageModule.objects.create(name="name")
        db = StorageModule.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")

    def test_str(self):
        sm = StorageModule.objects.create(name="name")
        db = StorageModule.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        s = str(sm)
        proper_str = f"{sm.id} - name"
        self.assertEqual(s, proper_str, "Error while creating string")
