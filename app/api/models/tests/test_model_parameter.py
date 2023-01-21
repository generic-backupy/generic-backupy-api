from django.db import IntegrityError
from django.test import TestCase

from api.models import Parameter

class TestModelParameter(TestCase):
    def setUp(self):
        db = Parameter.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-null constraint violated"):
            Parameter.objects.create(name=None, parameter=None)

    def test_create_required_fields_only(self):
        Parameter.objects.create(name="name", parameter={})
        db = Parameter.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name")
        self.assertEqual(db[0].parameter, {}, "Error in field 'parameter")
        self.assertIsNone(db[0].description, "Wrong default value in field 'description'")

    def test_create_all_fields(self):
        Parameter.objects.create(name="name", description="desc", parameter={})
        db = Parameter.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name")
        self.assertEqual(db[0].parameter, {}, "Error in field 'parameter")
        self.assertEqual(db[0].description,"desc", "Wrong default value in field 'description'")

    def test_delete(self):
        Parameter.objects.create(name="name", parameter={})
        db = Parameter.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")