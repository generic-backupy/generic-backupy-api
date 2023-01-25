from api.models import System
from api.serializers import (SystemBaseSerializer, SystemGetShortSerializer,
                             SystemListSerializer, SystemOnlyIdSerializer,
                             SystemPostSerializer, SystemRetrieveSerializer,
                             SystemSerializer)

from django.test import TestCase



class TestSystemSerializer(TestCase):
    def setUp(self):
        self.user = System.objects.create(
            name = 'test_system',
            description = 'test_description',
            host = 'test_host',
            additional_information = 'test_additional_information'
        )
 
    def test_system_post_serializer(self):
        serializer = SystemPostSerializer(self.user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['name'], 'test_system')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertEqual(serializer.data['host'], 'test_host')
        self.assertNotEqual(serializer.data['host'], 'wrong_host_name', "Error:  host name is not matched")
        self.assertEqual(serializer.data['additional_information'], 'test_additional_information')

    def test_system_retrieve_serializer(self):
        serializer = SystemRetrieveSerializer(self.user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['name'], 'test_system')
        self.assertEqual(serializer.data['description'], 'test_description')
        self.assertEqual(serializer.data['host'], 'test_host')
        self.assertEqual(serializer.data['additional_information'], 'test_additional_information')

    def test_system_base_serializer(self):
        serializer = SystemBaseSerializer(self.user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, {'id': self.user.pk, 'name': 'test_system'})

    def test_system_list_serializer(self):
        serializer = SystemListSerializer(self.user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, {'id': self.user.pk, 'name': 'test_system'})
        self.assertNotEqual(serializer.data['name'], 'wrong_host_name', "Error:  host name is not matched")

    def test_system_get_short_serializer(self):
        serializer = SystemGetShortSerializer(self.user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, {'id': self.user.pk, 'name': 'test_system'})

    def test_system_only_id_serializer(self):
        serializer = SystemOnlyIdSerializer(self.user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, {'id': self.user.pk})

