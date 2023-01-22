from django.test import TestCase
from api.models import Category, User
from django.db import IntegrityError


class TestModelBackup(TestCase):

    def setUp(self):
        db = Category.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            Category.objects.create(name=None)

    def test_create_required_fields_only(self):
        Category.objects.create(name="name")
        db = Category.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertIsNone(db[0].description, "Wrong default value in 'description'")

    def test_create_all_fields(self):
        Category.objects.create(name="name", description="desc")
        db = Category.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].description, "desc", "Error in field 'description'")

    def test_create_foreignkey(self):
        parent = Category.objects.create(name="parent")
        Category.objects.create(name="child", parent=parent)
        db = Category.objects.all()
        self.assertEqual(len(db), 2, "Object(s) not added to db")
        p = Category.objects.filter(name="parent")
        self.assertEqual(len(p), 1, "'parent' object not added to db")
        self.assertIsNone(p[0].parent, "Wrong default value in 'parent'")
        c = Category.objects.filter(name="child")
        self.assertEqual(len(c), 1, "'child' object not added to db")
        self.assertEqual(c[0].parent, parent, "Error in field 'parent'")

    def test_create_wrong_foreignkey(self):
        dummy = User.objects.create()
        db = User.objects.all()
        self.assertEqual(len(db), 1, "Dummy object not added to db")
        with self.assertRaises(ValueError, msg="Wrong data type not detected"):
            Category.objects.create(name="name", parent=dummy)



    def test_delete(self):
        Category.objects.create(name="name")
        db = Category.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")
