from django.test import TestCase
from django.db import IntegrityError
from api.models import Tag

class TestModelTag(TestCase):
    def setUp(self):
        db = Tag.objects.all()
        db.delete()
    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            Tag.objects.create(name=None)

    def test_create_required_field_only(self):
        Tag.objects.create(name="name")
        db = Tag.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertIsNone(db[0].description, "Wrong default value in 'description'")

    def test_create_all_fields(self):
        Tag.objects.create(name="name", description="desc")
        db = Tag.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].description, "desc", "Error in field 'description'")

    def test_delete(self):
        Tag.objects.create(name="name")
        db = Tag.objects.all()
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")
