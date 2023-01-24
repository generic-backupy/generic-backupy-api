from api.models import User
from api.serializers import (UserGetShortSerializer, UserListSerializer,
                             UserOnlyIdSerializer, UserPostSerializer,
                             UserRetrieveSerializer, UserSerializer,
                             UserShortListSerializer, UserUpdateSerializer)
from django.test import TestCase


class TestUserSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user',
            first_name='max',
            last_name='mustermann',
            email='test@user.com',
            password='testpassword'
        )

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'username': 'test_user'})

    def test_user_id_only_serializer(self):
        serializer = UserOnlyIdSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk})

    def test_user_post_serializer(self):
        serializer = UserPostSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'first_name': 'max', 'last_name': 'mustermann', 'email': 'test@user.com'})
