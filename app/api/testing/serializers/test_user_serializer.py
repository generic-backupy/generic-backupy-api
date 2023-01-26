from api.models import User
from api.serializers import (UserGetShortSerializer, UserOnlyIdSerializer,
                             UserPostSerializer, UserRetrieveSerializer,
                             UserSerializer, UserUpdateSerializer,
                             UserListSerializer)
from django.test import TestCase


class TestUserSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username = 'test_user',
            first_name = 'max',
            last_name = 'mustermann',
            email = 'test@user.com',
        )

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'username': 'test_user'})
        self.assertNotEqual(serializer.data['username'], 'WRONG_USERNAME')


    def test_user_id_only_serializer(self):
        serializer = UserOnlyIdSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk})

    def test_user_post_serializer(self):
        serializer = UserPostSerializer(self.user)
        self.assertEqual(serializer.data['first_name'], 'max')
        self.assertEqual(serializer.data['last_name'], 'mustermann')
        self.assertEqual(serializer.data['email'], 'test@user.com')
        self.assertNotEqual(serializer.data['email'], 'random@test.email')

    def test_user_update_serializer(self):
        serializer = UserUpdateSerializer(self.user)
        self.assertEqual(serializer.data['first_name'], 'max')
        self.assertNotEqual(serializer.data['first_name'], 'jon')
        self.assertEqual(serializer.data['last_name'], 'mustermann')
        self.assertNotEqual(serializer.data['last_name'], 'doe')
        self.assertEqual(serializer.data['email'], 'test@user.com')
        self.assertNotEqual(serializer.data['email'], 'random@test.email')

    def test_user_retrieve_serializer(self):
        serializer = UserRetrieveSerializer(self.user)
        self.assertEqual(serializer.data['username'], 'test_user')
        self.assertEqual(serializer.data['first_name'], 'max')
        self.assertEqual(serializer.data['last_name'], 'mustermann')
        self.assertEqual(serializer.data['email'], 'test@user.com')
        self.assertNotEqual(serializer.data['email'], 'random@test.email')

    def test_user_get_short_serializer(self):
        serializer = UserGetShortSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'username': 'test_user'})

    def test_user_list_serializer(self):
        serializer = UserListSerializer(self.user)
        self.assertEqual(serializer.data['username'], 'test_user')

