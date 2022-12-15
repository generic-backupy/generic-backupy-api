from api.views.base_view import UserCurrentConditionsPermission

from api.views import BaseViewSet
from django.test import TestCase

from api.models import Secret, BackupJob, BackupJobSecret
from django.utils import timezone


# models test
from api.serializers import SecretGbModuleSerializer, BackupJobSecretGbModuleSerializer
from api.utils.backup_job_util import BackupJobUtil



class BaseViewTest(TestCase):

    def setUp(self):
        pass

    def test_get_additional_permission_classes(self):
        # fill database
        base_view = BaseViewSet()
        # assert
        self.assertEqual(base_view.get_additional_permission_classes(), (UserCurrentConditionsPermission,))
