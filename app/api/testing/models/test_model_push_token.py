from django.test import TestCase, TransactionTestCase

from api.models import PushToken, User
from django.db import IntegrityError
from knox.models import AuthToken


def create_user_auth_token():
    u = User.objects.create_user(username="user")
    auth = AuthToken.objects.create(u)
    return auth[0]


class TestModelPushToken(TestCase):
    def setUp(self):
        db = PushToken.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-null constraint violated"):
            PushToken.objects.create(key=None, auth_token=None)

    def test_create_required_fields_only(self):
        auth = create_user_auth_token()
        PushToken.objects.create(key="key", auth_token=auth)
        db = PushToken.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].key, "key", "Error in field 'key'")

    def test_create_wrong_foreignkey(self):
        dummy = User.objects.create()
        with self.assertRaises(ValueError, msg="Wrong data type detected"):
            PushToken.objects.create(key="key", auth_token=dummy)

    def test_delete(self):
        auth = create_user_auth_token()
        PushToken.objects.create(key="key", auth_token=auth)
        db = PushToken.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")


class TestModelPushTokenTrans(TransactionTestCase):

    def test_uniqueness(self):
        auth = create_user_auth_token()
        PushToken.objects.create(key="key", auth_token=auth)
        db = PushToken.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        PushToken.objects.create(key="other_key", auth_token=auth)
        db = PushToken.objects.all()
        self.assertEqual(len(db), 2, "Second object not added to db")
        with self.assertRaises(IntegrityError, msg="Uniqueness constraints violated"):
            PushToken.objects.create(key="key", auth_token=auth)
