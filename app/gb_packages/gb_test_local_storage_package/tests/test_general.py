from unittest import TestCase

from gb_module.testing.util.module_test_util import ModuleTestUtil
from gb_module.testing.util.backup_result_test_util import *
from ..gb_module import *
import os
import shutil

# models test
class GeneralTest(TestCase):
    module: GBModule = None
    backup_location = "backup"
    backup_location_temp = "backup/temp"
    backup_location_temp_test_file = "backup/temp/test.bk"

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(GeneralTest.backup_location):
            os.mkdir(GeneralTest.backup_location)
        if not os.path.exists(GeneralTest.backup_location_temp):
            os.mkdir(GeneralTest.backup_location_temp)
        with open(GeneralTest.backup_location_temp_test_file, "w") as file:
            file.write("hello backup from temp :)")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(GeneralTest.backup_location):
            shutil.rmtree(GeneralTest.backup_location, ignore_errors=True)

    def setUp(self):
        self.module = ModuleTestUtil.create_storage_module(GBModule, self.backup_location)
        self.backup_raw = BackupResultTestUtil.create_result_raw_backup()
        self.backup_temp_location_wrong = BackupResultTestUtil.create_result_backup_temp_location("/wrong-location")
        self.backup_temp_location_correct = BackupResultTestUtil.create_result_backup_temp_location(GeneralTest.backup_location_temp_test_file)

    def test_module_creation(self):
        self.assertIsNotNone(self.module, "Object is not allowed to be None")

    def test_no_path(self):
        self.module.parameters = None
        response = self.module.save_to_storage(self.backup_raw)
        self.assertIsNotNone(response.error, "Response should contains a no path error")

    def test_save_backup_raw_to_storage(self):
        response = self.module.save_to_storage(self.backup_raw)
        self.assertIsNone(response.error, "Storage Error")
        self.assertIsNotNone(response)
        self.assertTrue(os.path.exists(response.path), "Response Path doesn't exist")

    def test_save_temp_backup_wrong_location_to_storage(self):
        response = self.module.save_to_storage(self.backup_temp_location_wrong)
        self.assertIsNotNone(response.error, "Storage Error")

    def test_save_temp_backup_correct_location_to_storage(self):
        response = self.module.save_to_storage(self.backup_temp_location_correct)
        self.assertIsNone(response.error, "Storage Error")
