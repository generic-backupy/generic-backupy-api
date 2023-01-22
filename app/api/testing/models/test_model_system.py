from django.test import TestCase
from api.models import System, Category, User
from django.db import IntegrityError


class TestModelBackup(TestCase):

    def setUp(self):
        db = System.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            System.objects.create(name=None)

    def test_create_required_fields_only(self):
        System.objects.create(name="name")
        db = System.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertIsNone(db[0].description, "Wrong default value in 'description'")
        self.assertIsNone(db[0].additional_information, "Wrong default value in 'additional_information'")
        self.assertIsNone(db[0].category, "Wrong default value in 'category'")

    def test_create_all_fields(self):
        System.objects.create(name="name", description="desc", additional_information="info")
        db = System.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].description, "desc", "Error in field 'description'")
        self.assertEqual(db[0].additional_information, "info", "Error in field 'additional_information'")
        self.assertIsNone(db[0].category, "Wrong default value in 'category'")

    def test_create_foreignkey(self):
        cat = Category.objects.create(name="name")
        dummy_db = Category.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object not added to db")
        System.objects.create(name="name", category=cat)
        db = System.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].category, cat, "Error in field 'category")


    def test_create_wrong_foreignkey(self):
        dummy = User.objects.create()
        dummy_db = User.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object not added to db")
        with self.assertRaises(ValueError, msg="Wrong data type not detected"):
            System.objects.create(name="name", category=dummy)

    def test_delete(self):
        System.objects.create(name="name")
        db = System.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")
