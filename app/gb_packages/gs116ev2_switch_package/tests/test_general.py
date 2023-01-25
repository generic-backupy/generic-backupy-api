from unittest import TestCase
from unittest.mock import patch, Mock
import time
from gb_module.utils.selenium_util import SeleniumUtil

from gb_module.testing.util.module_test_util import ModuleTestUtil
from ..gb_module import *

class GeneralTest(TestCase):
    module: GBModule = None

    def setUp(self):
        self.module = ModuleTestUtil.create_default_module(GBModule)

    def test_module_creation(self):
        self.assertIsNotNone(self.module, "Object is not allowed to be None")

    def test_no_password(self):
        self.module.secrets = None
        response = self.module.do_backup()
        self.assertIsNotNone(response.error, "Response should contains a no password error")

    @patch.object(BackupFetcher, 'restore_backup')
    def test_do_restore_general(self, mock_restore_backup):
        response = self.module.do_restore(RetrieveResult())
        self.assertIsNone(response.error, "Response shouldn't contains an error")
        self.assertTrue(mock_restore_backup.called)

    @patch.object(SeleniumUtil, 'get_options_with_download_path', return_value=Mock())
    @patch.object(time, 'sleep', return_value=Mock())
    def test_restore_backup_util_method(self, options_call, sleep_call):
        BackupFetcher.restore_backup("", "", "", "", "", "", "")
        self.assertTrue(options_call.called)
        self.assertTrue(sleep_call.called)

    """def test_real_device(self):
        # enter the real credentials
        self.module.secrets |= {'password': ''}
        self.module.parameters |= {
            'host': '',
            "switch_type": "GS305E",
            "login_input_id": "password",
            "login_button_id": "loginBtn",
            "backup_endpoint": "backup_conf.cgi?cmd=backup_conf"
        }
        
        # run the test
        response = self.module.do_backup()
        self.assertIsNone(response.error)
        self.assertIsNotNone(response.backup_temp_location, "Response should contains a backup_temp_location")
"""
