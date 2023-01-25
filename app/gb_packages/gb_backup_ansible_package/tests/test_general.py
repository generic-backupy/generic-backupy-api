from unittest import TestCase

from gb_module.testing.util.module_test_util import ModuleTestUtil
from gb_module.testing.util.backup_result_test_util import *
from module import *
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
