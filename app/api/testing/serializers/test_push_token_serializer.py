from api.models import PushToken
from api.serializers import PushTokenPostSerializer,PushTokenOnlyIdSerializer
from django.test import TestCase


class TestPushTokenSerializer(TestCase):
    def setUp(self):
        self.user = PushToken.objects.create(
            key = 'test_key',
        )
