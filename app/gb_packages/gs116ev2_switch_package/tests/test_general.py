from unittest import TestCase

from gb_module.gb_module.testing.util.module_test_util import ModuleTestUtil
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
