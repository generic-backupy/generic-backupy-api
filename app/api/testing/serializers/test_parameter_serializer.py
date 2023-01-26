from api.models import Parameter
from api.serializers import (ParameterBaseSerializer,
                             ParameterGbModuleSerializer,
                             ParameterGetShortSerializer,
                             ParameterListSerializer,
                             ParameterOnlyIdSerializer,
                             ParameterPostSerializer,
                             ParameterRetrieveSerializer, ParameterSerializer)

from django.test import TestCase


class TestParameterSerializer(TestCase):
    def setUp(self):
        self.user = Parameter.objects.create(
            name = 'test_',
            description = 'test_description',
            parameter = {'a':1,'b':2},
        )

    def test_parameter_base_serializer(self):
        serializer = ParameterBaseSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')


    def test_parameter_serializer(self):
        serializer = ParameterSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_', 'description': 'test_description', 'parameter': {'a':1,'b':2}})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')
        self.assertNotEqual(serializer.data['parameter'], {'a':1,'c':9})

    def test_parameter_id_only_serializer(self):
        serializer = ParameterOnlyIdSerializer(self.user)
        self.assertEqual(serializer.data, {'id': self.user.pk})


    def test_parameter_list_serializer(self):
        serializer = ParameterListSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')

    def test_parameter_get_short_serializer(self):
        serializer = ParameterGetShortSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_'})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')

    def test_parameter_gb_module_serializer(self):
        serializer = ParameterGbModuleSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_', 'description': 'test_description', 'parameter': {'a':1,'b':2}})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')
        self.assertNotEqual(serializer.data['parameter'], {'a':1,'c':9})

    def test_parameter_post_serializer(self):
        serializer = ParameterPostSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_', 'description': 'test_description', 'parameter': {'a':1,'b':2}})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')
        self.assertNotEqual(serializer.data['parameter'], {'a':1,'c':9})

    def test_parameter_retrieve_serializer(self):
        serializer = ParameterRetrieveSerializer(self.user)
        self.assertEqual(serializer.data, {
                         'id': self.user.pk, 'name': 'test_', 'description': 'test_description', 'parameter': {'a':1,'b':2}})
        self.assertNotEqual(serializer.data['name'], 'wrong_name')
        self.assertNotEqual(serializer.data['description'], 'unmatching_description')
        self.assertNotEqual(serializer.data['parameter'], {'a':1,'c':9})

