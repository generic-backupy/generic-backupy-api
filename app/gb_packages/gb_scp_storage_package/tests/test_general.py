from unittest import TestCase
from unittest.mock import patch, Mock
from django.utils import timezone

from gb_module.gb_module.testing.util.module_test_util import ModuleTestUtil
from gb_module.gb_module.testing.util.backup_result_test_util import *
from ..gb_module import *
import os
import shutil

# models test
class GeneralTest(TestCase):
    module: GBModule = None
    backup_path = "/home/test/backups"
    backup_username = "test"
    backup_host = "10.12.34.56"
    private_key = """-----BEGIN OPENSSH PRIVATE KEY-----
test
-----END OPENSSH PRIVATE KEY-----"""

    def setUp(self):
        self.module = ModuleTestUtil.create_storage_module(GBModule, self.backup_path)
        self.module.parameters.append(ModuleTestUtil.create_parameter("username", self.backup_username))
        self.module.parameters.append(ModuleTestUtil.create_parameter("host", self.backup_host))
        self.module.secrets.append(ModuleTestUtil.create_secret("private_key", self.private_key))
        self.backup_raw = BackupResultTestUtil.create_result_raw_backup()

    def test_module_creation(self):
        self.assertIsNotNone(self.module, "Object is not allowed to be None")

    def test_no_path(self):
        self.module.parameters = None
        response = self.module.save_to_storage(self.backup_raw)
        self.assertIsNotNone(response.error, "Response should contains a no path error")

    @patch.object(subprocess, 'run', return_value=Mock(stderr=b"any error"))
    def test_subprocess_error(self, mock):
        response = self.module.save_to_storage(self.backup_raw)
        self.assertTrue(mock.called)
        self.assertIsNotNone(response.error, "Storage Error")

    @patch.object(subprocess, 'run', return_value=Mock(stderr=b""))
    def test_save_backup_success(self, mock):
        response = self.module.save_to_storage(self.backup_raw)
        self.assertIsNone(response.error, "Storage Error")
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.path)
        self.assertTrue(mock.called)

    """def test_real_test(self):
        response = self.module.save_to_storage(self.backup_raw)
        self.assertIsNone(response.error, "Storage Error")
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.path)"""
