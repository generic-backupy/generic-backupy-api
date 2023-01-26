from api.models import Secret
from api.serializers import (SecretBaseSerializer, SecretGbModuleSerializer,
                             SecretGetShortSerializer, SecretListSerializer,
                             SecretOnlyIdSerializer, SecretPostSerializer,
                             SecretRetrieveSerializer, SecretSerializer)

from django.test import TestCase


class TestSecretSerializer(TestCase):
    def setUp(self):
        self.user = Secret.objects.create(
            name = 'test_',
            description = 'test_description',
            secret = 'test_secret',
        )

    def test_secret_base_serializer(self):
        serializer = SecretBaseSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')

    def test_secret_retrieve_serializer(self):
        serializer = SecretRetrieveSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['secret'], 'wrong_secret')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')
        self.assertEqual(serializer.data['id'],  self.user.pk)


    def test_secret_id_only_serializer(self):
        serializer = SecretOnlyIdSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk})

    def test_secret_list_serializer(self):
        serializer = SecretListSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')

    def test_secret_get_short_serializer(self):
        serializer = SecretGetShortSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')


    def test_secret_serializer(self):
        serializer = SecretSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['secret'], 'wrong_secret')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')
        self.assertEqual(serializer.data['id'],  self.user.pk)

    def test_secret_gb_module_serializer(self):
        serializer = SecretGbModuleSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['secret'], 'wrong_secret')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')
        self.assertEqual(serializer.data['id'],  self.user.pk)

    def test_secret_post_serializer(self):
        serializer = SecretPostSerializer(self.user)
        self.assertEqual(serializer.data['name'], 'test_')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['secret'], 'wrong_secret')
        self.assertNotEqual(serializer.data['description'], 'wrong_descrirtion')
        self.assertEqual(serializer.data['id'],  self.user.pk)

