from django.test import TestCase

from api.models import User

from django.db import IntegrityError, DataError


# Create your tests here.
class TestModelUser(TestCase):

    def setUp(self):
        db = User.objects.all()
        db.delete()

    def test_create_defaults(self):
        u = User.objects.create()
        db = User.objects.all()
        self.assertEqual(len(db), 1, "object not saved")
        self.assertEqual(db[0].created_language, "en", "Wrong default value in 'created_language'")
        self.assertIsNone(db[0].email_verification_code, "Wrong default value in 'email_verification_code'")
        self.assertFalse(db[0].email_verified, "Wrong default value in 'email_verified'")

    def test_create_char_fields_only(self):
        u = User.objects.create(
            email_verification_code="123", privacy_version="123", conditions_version="123", created_language="pl")
        db = User.objects.all()
        self.assertEqual(len(db), 1, "object not saved")
        self.assertEqual(db[0].email_verification_code, "123", "Error in field 'email_verification_code'")
        self.assertEqual(db[0].privacy_version, "123", "Error in field 'privacy_version'")
        self.assertEqual(db[0].conditions_version, "123", "Error in field 'conditions_version'")
        self.assertEqual(db[0].created_language, "pl", "Error in field 'created_language'")
        self.assertFalse(db[0].email_verified, "Wrong default value in 'email_verified'")

    def test_create_bool_fields_only(self):
        u = User.objects.create(email_verified=True)
        db = User.objects.all()
        self.assertTrue(db[0].email_verified, "Error in field 'email_verified'")
        self.assertEqual(db[0].created_language, "en", "Wrong default value in 'created_language'")

    def test_constraints(self):
        with self.assertRaises(DataError, msg="Constraints Validated (too long str in 'privacy_version'"):
            u = User.objects.create(privacy_version="1234567")

    def test_delete(self):
        u = User.objects.create()
        db = User.objects.all()
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")

    def test_unique(self):
        u1 = User.objects.create(email_verification_code="1")
        with self.assertRaises(IntegrityError, msg="Uniqueness constraints validated"):
            u2 = User.objects.create(email_verification_code="1")






