from django.test import TestCase
from api.models import Secret
from django.db import IntegrityError


class TestModelBackup(TestCase):

    def setUp(self):
        db = Secret.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            Secret.objects.create(name=None)

    def test_create_required_fields_only(self):
        Secret.objects.create(name="name")
        db = Secret.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertIsNone(db[0].description, "Wrong default value in 'description'")

    def test_create_all_fields(self):
        Secret.objects.create(name="name", description="desc", secret="info")
        db = Secret.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].description, "desc", "Error in field 'description'")
        self.assertEqual(db[0].secret, "info", "Error in field 'secret'")

    def test_delete(self):
        Secret.objects.create(name="name")
        db = Secret.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")

    def test_str(self):
        secret = Secret.objects.create(name="name")
        db = Secret.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        s = str(secret)
        proper_str = f"{secret.id} - name"
        self.assertEqual(s, proper_str, "Error while creating string")
