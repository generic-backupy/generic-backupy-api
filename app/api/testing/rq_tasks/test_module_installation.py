import time
from unittest.mock import patch, Mock

from api.testing.test_utils.backup_job_test_util import BackupJobTestUtil

from api.models import Backup, RestoreExecution, BackupModule, StorageModule, \
    BackupJobStorageModule, BackupExecution, ModuleInstallationExecution
from api.testing.test_utils.module_test_util import ModuleTestUtil
from api.utils.package_util import PackageUtil
from django.test import TestCase
from gb_module.gb_module.core.base_result import BaseResult
from api.rq_tasks.module_installation import install_module
import os


class TestModuleInstallation(TestCase):

    def setUp(self) -> None:
        self.module_installation_execution = ModuleInstallationExecution()

    def test_installation_invalid_path(self):
        install_module("api/testing/test_files/module.zip", self.module_installation_execution)
        self.assertEqual(self.module_installation_execution.state, 2)

    def test_installation_with_zip(self):
        filename = f"{time.time()}-module.zip"
        os.system(f"cp api/testing/test_files/module.zip /packages/{filename}")
        install_module(filename, self.module_installation_execution)
        self.assertEqual(self.module_installation_execution.state, 3)
        self.assertEqual(BackupModule.objects.last().file_system_path, f"/packages/{filename.replace('.zip', '-unzipped')}")
        for f in os.listdir("/packages"):
            if f != ".gitkeep":
                os.system(f"rm -rf {f}")

