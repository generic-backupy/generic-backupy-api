from unittest.mock import patch, Mock

from api.testing.test_utils.backup_job_test_util import BackupJobTestUtil

from api.models import Category, Backup, RestoreExecution, BackupModule, BackupExecution, StorageModule, \
    BackupJobStorageModule
from api.rq_tasks.restore import restore
from api.testing.test_utils.category_test_util import CategoryTestUtil
from api.utils.backup_util import BackupUtil
from api.utils.category_util import CategoryUtil
from api.utils.package_util import PackageUtil

from api.views.base_view import UserCurrentConditionsPermission

from api.views import BaseViewSet, CategoryViewSet
from django.test import TestCase
from api.utils.ExecutionUtil import ExecutionUtil


class TestPackageUtil(TestCase):

    def setUp(self) -> None:
        self.backup_1 = Backup.objects.create(name="Test")
        self.valid_module = BackupModule.objects.create(name="valid", file_system_path="api/testing/test_files/mock_module")
        self.invalid_module = BackupModule.objects.create(name="invalid", file_system_path="gb_packages/invalid")
        self.valid_storage_module = StorageModule.objects.create(name="valid", file_system_path="api/testing/test_files/mock_module")
        self.execution_instance = RestoreExecution.objects.create()
        self.job_switch_1, self.job_switch_2, self.job_access_point, self.job_special_switch_2 = BackupJobTestUtil.create_network_test_backup_jobs()
        self.job_switch_1.backup_module_direct_parameters = {"test": 12}
        self.backup_job_storage_module_pivot = BackupJobStorageModule.objects.create(backup_job=self.job_switch_1, storage_module=self.valid_storage_module)
        self.backup_job_storage_module_pivot.direct_parameters = {"test": 12}

    def test_get_package_instance_or_error(self):
        package_instance = PackageUtil.get_package_instance_or_error(self.execution_instance, self.valid_module)
        self.assertIsNotNone(package_instance, "package_instance should not be None")
        self.assertIsNone(self.execution_instance.errors, "There shouldn't be any errors in the execution")

    def test_get_package_instance_or_error_file_not_found(self):
        package_instance = PackageUtil.get_package_instance_or_error(self.execution_instance, self.invalid_module)
        self.assertIsNone(package_instance, "package_instance should be None")
        self.assertIsNotNone(self.execution_instance.errors, "There should be any error in the execution")

    def test_inject_module_log_function(self):
        package_instance = PackageUtil.get_package_instance_or_error(self.execution_instance, self.valid_module)
        PackageUtil.inject_module_log_function(package_instance, self.execution_instance)
        self.assertIsNone(self.execution_instance.logs)
        package_instance.log("test")
        self.assertIsNotNone(self.execution_instance.logs)

    def test_inject_backup_parameters(self):
        package_instance = PackageUtil.get_package_instance_or_error(self.execution_instance, self.valid_module)
        self.assertIsNone(package_instance.parameters.get("test"))
        PackageUtil.inject_backup_parameters(package_instance, self.job_switch_1, {"test2": 1})
        self.assertIsNotNone(package_instance.parameters.get("test"))
        self.assertIsNotNone(package_instance.parameters.get("test2"))

    def test_inject_storage_parameters(self):
        package_instance = PackageUtil.get_package_instance_or_error(self.execution_instance, self.valid_storage_module)
        self.assertIsNone(package_instance.parameters.get("test"))
        PackageUtil.inject_storage_parameters(package_instance, self.job_switch_1, self.backup_job_storage_module_pivot, {"test2": 1})
        self.assertIsNotNone(package_instance.parameters.get("test"))
        self.assertIsNotNone(package_instance.parameters.get("test2"))
