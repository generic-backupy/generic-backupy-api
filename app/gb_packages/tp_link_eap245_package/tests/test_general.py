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

"""
    def test_real_device(self):
        # enter the real credentials
        self.module.secrets |= {
            'username': '',
            'password': ''
        }
        self.module.parameters |= {
            'host': ''
        }
        
        # run the test
        response = self.module.do_backup()
        self.assertIsNone(response.error)
        self.assertIsNotNone(response.backup_temp_location, "Response should contains a backup_temp_location")
"""
