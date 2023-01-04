from unittest import TestCase
from unittest.mock import patch, Mock

from gb_module.gb_module.testing.util.module_test_util import ModuleTestUtil
from gb_module.gb_module.testing.util.backup_result_test_util import *
from ..gb_module import *

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
        self.module.parameters |= {
            "username": self.backup_username,
            "host": self.backup_host,
            "private_key": self.private_key
        }
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

    @patch.object(subprocess, 'run', return_value=Mock(stderr=b""))
    def test_save_backup_success(self, mock):
        self.module.retrieve_path = "/"
        response = self.module.retrieve_from_storage()
        self.assertIsNone(response.error, "Storage Error")
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.backup_temp_location)
        self.assertTrue(mock.called)

    """def test_real_test(self):
        response = self.module.save_to_storage(self.backup_raw)
        self.assertIsNone(response.error, "Storage Error")
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.path)"""
