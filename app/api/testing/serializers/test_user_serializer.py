from api.serializers import UserSerializer
from django.test import TestCase
from api.models import User

class TestUserSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user',
            email='test@user.com',
            password='testpassword'
        )
    
    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk, 'username': 'test_user'})