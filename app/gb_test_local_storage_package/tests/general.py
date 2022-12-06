from unittest import TestCase
from django.utils import timezone

from gb_module.gb_module.testing.util.module_test_util import ModuleTestUtil
from gb_module.gb_module.testing.util.backup_result_test_util import *
from ..gb_module import *
import os
import shutil

# models test
class GeneralTest(TestCase):
    module: GBModule = None
    backup_location = "backup"

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(GeneralTest.backup_location):
            os.mkdir(GeneralTest.backup_location)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(GeneralTest.backup_location):
            #shutil.rmtree(GeneralTest.backup_location, ignore_errors=True)
            pass

    def setUp(self):
        # backup locations
        self.backup_location_temp = "backup/temp"

        self.module = ModuleTestUtil.create_storage_module(GBModule, self.backup_location)
        self.backup_raw = BackupResultTestUtil.create_result_raw_backup()
        self.backup_temp_location_wrong = BackupResultTestUtil.create_result_backup_temp_location("/wrong-location")
        self.backup_temp_location_wrong = BackupResultTestUtil.create_result_backup_temp_location(self.backup_location_temp)

    def test_module_creation(self):
        self.assertIsNotNone(self.module, "Object is not allowed to be None")

    def test_no_path(self):
        self.module.parameters = None
        response = self.module.save_to_storage(self.backup_raw)
        self.assertIsNotNone(response.error, "Response should contains a no path error")

    def test_save_to_storage(self):
        print(f"our path: {os.getcwd()}\n{os.listdir()}")
        response = self.module.save_to_storage(self.backup_raw)
        self.assertIsNone(response.error, "Storage Error")
        self.assertIsNotNone(response)
        print(f"path: {response.path}")
        self.assertTrue(os.path.exists(response.path), "Response Path doesn't exist")

