from django.test import TestCase

from api.models import Secret, BackupJob, BackupJobSecret
from django.utils import timezone


# models test
from api.serializers import SecretGbModuleSerializer, BackupJobSecretGbModuleSerializer
from api.utils.backup_job_util import BackupJobUtil


class GeneralUtilTest(TestCase):

    def setUp(self):
        pass

    def test_g(self):
        # fill database
        secret = Secret.objects.create(name="TestSecret", secret="pssst")
        backup_job = BackupJob.objects.create(name="Test")
        backup_job_secret = BackupJobSecret.objects.create(backup_job=backup_job, secret=secret, key="password")

        # fetch job and secrets
        secrets = BackupJobUtil.parsed_secret_array(BackupJob.objects.all()[0])

        # assert
        self.assertEqual(len(secrets), 1)
        self.assertDictEqual(secrets[0], {"id": 1, "name": "TestSecret", "secret": "pssst", "key": "password"})
