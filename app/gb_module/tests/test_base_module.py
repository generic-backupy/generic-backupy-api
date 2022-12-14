from unittest import TestCase
from django.utils import timezone
from gb_module.gb_module.core.base_module import BaseModule

from gb_module.gb_module.testing.util.module_test_util import ModuleTestUtil
from gb_module.gb_module.testing.util.backup_result_test_util import *
from ..gb_module import *
import os
import shutil

# models test
class TestBaseModule(TestCase):
    module: BaseModule = None
    temp_test_path = '/opt/test'

    def setUp(self):
        self.module = BaseModule()

    def tearDown(self):
        shutil.rmtree(self.temp_test_path, ignore_errors=True)

    def test_module_creation(self):
        self.assertIsNotNone(self.module, "Object is not allowed to be None")

    def test_set_temp_path(self):
        self.module.set_temp_path(self.temp_test_path)
        self.assertEqual(self.temp_test_path, self.module.temp_path, "different temp_path after changing it")
        self.assertTrue(os.path.exists(self.temp_test_path), "created temp_path doesn't exist")

    def test_(self):
        temp_folder_path = self.module.get_temp_folder_path("test")
        self.assertTrue(temp_folder_path.startswith(self.module.temp_path), "temp folder path should start with the temp_path")

    def test_get_host_out_of_params(self):
        self.module.system["host"] = "testsystem"
        self.module.parameters["host"] = "testparam"
        self.assertEqual(self.module.get_host(), "testparam", "Host should be fetched from params")

    def test_get_host_out_of_system(self):
        self.module.system["host"] = "testsystem"
        self.assertEqual(self.module.get_host(), "testsystem", "Host should be fetched from params")
