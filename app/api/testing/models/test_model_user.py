from django.test import TransactionTestCase, TestCase
from knox.models import AuthToken

from api.models import User, PushToken

from django.db import IntegrityError, DataError


class TestModelUser(TestCase):

    def setUp(self):
        db = User.objects.all()
        db.delete()

    def test_create_defaults(self):
        User.objects.create()
        db = User.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].created_language, "en", "Wrong default value in 'created_language'")
        self.assertIsNone(db[0].email_verification_code, "Wrong default value in 'email_verification_code'")
        self.assertFalse(db[0].email_verified, "Wrong default value in 'email_verified'")

    def test_create_char_fields_only(self):
        User.objects.create(
            email_verification_code="123", privacy_version="123", conditions_version="123", created_language="pl")
        db = User.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].email_verification_code, "123", "Error in field 'email_verification_code'")
        self.assertEqual(db[0].privacy_version, "123", "Error in field 'privacy_version'")
        self.assertEqual(db[0].conditions_version, "123", "Error in field 'conditions_version'")
        self.assertEqual(db[0].created_language, "pl", "Error in field 'created_language'")
        self.assertFalse(db[0].email_verified, "Wrong default value in 'email_verified'")

    def test_create_bool_fields_only(self):
        User.objects.create(email_verified=True)
        db = User.objects.all()
        self.assertTrue(db[0].email_verified, "Error in field 'email_verified'")
        self.assertEqual(db[0].created_language, "en", "Wrong default value in 'created_language'")

    def test_create_fields_parent_class(self):
        # parent class comes from package, therefore it doesn't have to be tested deeply
        User.objects.create(username="name")
        db = User.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].username, "name", "Error in field 'username")

    def test_constraints(self):
        with self.assertRaises(DataError, msg="Constraints Validated (too long str in 'privacy_version'"):
            User.objects.create(privacy_version="1234567")

    def test_delete(self):
        User.objects.create()
        db = User.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")

    def test_create_email_verification_code(self):
        u = User.objects.create(username="user")
        verification_code, now = u.create_email_verification_code()
        self.assertIsInstance(verification_code, str, "Error while creating verification code: wrong type")
        self.assertEqual(len(verification_code), 32, "Error while creating verification code: too short")
        db = User.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].email_verification_code, verification_code, "Error in field 'verification_code'")
        self.assertEqual(db[0].email_verification_code_created_at, now, "Error in field 'verification_code'")
        u = User.objects.create(username="user2", email_verification_code="1")
        verification_code, _ = u.create_email_verification_code(save=False)
        db = User.objects.all()
        self.assertEqual(len(db), 2, "Object not added to db")
        self.assertEqual(db[1].email_verification_code, "1",
                         "Error in field 'verification_code' - not supposed to change")
        u = User.objects.create(username="user3", email_verification_code="2")
        verification_code, _ = u.create_email_verification_code(save=True)
        db = User.objects.all()
        self.assertEqual(len(db), 3, "Object not added to db")
        self.assertEqual(db[2].email_verification_code, verification_code,
                         "Error in field 'verification_code' - supposed to change")

    def test_get_push_token(self):
        u = User.objects.create(username="user")
        token = u.get_push_tokens()
        token = str(token)
        proper_ans = "<QuerySet []>"
        self.assertEqual(token, proper_ans, "Error while retrieving push tokens (empty)")
        auth = AuthToken.objects.create(u)[0]
        PushToken.objects.create(key="key", auth_token=auth)
        token = u.get_push_tokens()
        token = str(token)
        proper_ans = "<QuerySet ['key']>"
        self.assertEqual(token, proper_ans,"Error while retrieving push tokens (one el)")
        PushToken.objects.create(key="key2", auth_token=auth)
        token = u.get_push_tokens()
        token = str(token)
        proper_ans = "<QuerySet ['key', 'key2']>"
        self.assertEqual(token, proper_ans,"Error while retrieving push tokens (many els)")


class TestModelUserTrans(TransactionTestCase):
    def test_unique(self):
        User.objects.create(username="name")
        db = User.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        with self.assertRaises(IntegrityError, msg="Uniqueness constraints violated (username)"):
            User.objects.create(username="name")
        User.objects.create(username="other_name")
        db = User.objects.all()
        self.assertEqual(len(db), 2, "Second object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")
        User.objects.create(username="name", email_verification_code="1")
        User.objects.create(username="other_name", email_verification_code="2")
        db = User.objects.all()
        self.assertEqual(len(db), 2, "Object(s) not added to db")
        with self.assertRaises(IntegrityError, msg="Uniqueness constraints violated (email_verification_code)"):
            User.objects.create(username="third_name", email_verification_code="1")
