from unittest import TestCase
from unittest.mock import patch, Mock

from gb_module.testing.util.module_test_util import ModuleTestUtil
from gb_module.testing.util.backup_result_test_util import *
from ..module import *
import os

# models test
class GeneralTest(TestCase):
    def setUp(self):
        # backup locations
        self.backup_location = "backup"
        self.backup_location_temp = "backup/temp"
        if not os.path.exists(self.backup_location):
            os.mkdir(self.backup_location)

        self.module = ModuleTestUtil.create_storage_module(GBModule, self.backup_location)
        self.backup_raw = BackupResultTestUtil.create_result_raw_backup()
        self.backup_temp_location_wrong = BackupResultTestUtil.create_result_backup_temp_location("/wrong-location")
        self.backup_temp_location_wrong = BackupResultTestUtil.create_result_backup_temp_location(self.backup_location_temp)

    def test_module_creation(self):
        self.assertIsNotNone(self.module, "Object is not allowed to be None")

    def test_save_to_storage(self):
        print(f"our path: {os.getcwd()}\n{os.listdir()}")
        response = self.module.do_backup()
        self.assertIsNotNone(response)

    @patch.object(subprocess, "run")
    def test_do_backup(self, mock_subprocess_run):
        mock_subprocess_run.return_value = Mock(stderr=None, stdout="Success")
        self.module.parameters |= {
            "inventory": "inventory",
            "playbook": "playbook",
            "private_key": "private_key"
        }
        response = self.module.do_backup()
        self.assertEqual(response.error, "Error at download process!")
        self.assertTrue(mock_subprocess_run.called)

    @patch.object(subprocess, "run")
    def test_do_restore(self, mock_subprocess_run):
        mock_subprocess_run.return_value = Mock(stderr=None, stdout="Success")
        mock_retrieve_result = Mock(backup_temp_location="test")
        self.module.parameters |= {
            "inventory": "inventory",
            "playbook": "playbook",
            "private_key": "private_key"
        }
        response = self.module.do_restore(mock_retrieve_result)
        self.assertIsNone(response.error)
        self.assertTrue(mock_subprocess_run.called)
