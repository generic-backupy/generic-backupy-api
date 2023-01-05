from unittest.mock import patch, Mock

from api.testing.test_utils.backup_job_test_util import BackupJobTestUtil

from api.models import Backup, RestoreExecution, BackupModule, StorageModule, \
    BackupJobStorageModule, BackupExecution
from api.testing.test_utils.module_test_util import ModuleTestUtil
from api.utils.package_util import PackageUtil
from django.test import TestCase
from gb_module.gb_module.core.base_result import BaseResult
from api.rq_tasks.restore import restore
from api.rq_tasks.backup import backup


class TestRestore(TestCase):

    def setUp(self) -> None:
        self.restore_execution = RestoreExecution.objects.create()

        self.job_switch_1, self.job_switch_2, self.job_access_point, self.job_special_switch_2 = BackupJobTestUtil.create_network_test_backup_jobs()
        self.backup_1 = Backup.objects.create(name="Test", backup_job=self.job_switch_1)
        self.backup_execution = BackupExecution.objects.create(backup_job=self.job_switch_1)

        #restore.delay(backup_obj, user, restore_execution)
        #self.restore_execution =

        self.valid_backup_module = ModuleTestUtil.create_backup_mock_module()
        self.invalid_module = ModuleTestUtil.create_invalid_backup_module()
        self.valid_storage_module = ModuleTestUtil.create_storage_mock_module()

        self.job_switch_1.backup_module_direct_parameters = {"test": 12}
        self.backup_job_storage_module_pivot = BackupJobStorageModule.objects.create(backup_job=self.job_switch_1, storage_module=self.valid_storage_module)
        self.backup_job_storage_module_pivot.direct_parameters = {"test": 12}

    def test_full_backup_and_restore(self):
        old_amount_of_backups = len(Backup.objects.all())
        # do backup
        backup(self.job_switch_1, self.valid_backup_module, [self.backup_job_storage_module_pivot], None, self.backup_execution)
        self.assertGreater(len(Backup.objects.all()), old_amount_of_backups)
        # do restore out of the backup
        restore(Backup.objects.last(), None, self.restore_execution)
        self.assertEqual(self.restore_execution.state, 3)

    def test_full_restore_missing_backup(self):
        old_amount_of_backups = len(Backup.objects.all())
        # do backup
        backup(self.job_switch_1, self.valid_backup_module, [self.backup_job_storage_module_pivot], None, self.backup_execution)
        self.assertGreater(len(Backup.objects.all()), old_amount_of_backups)
        # do restore out of the backup
        last_backup = Backup.objects.last()
        last_backup.path += "invalid.bk"
        last_backup.save()
        restore(last_backup, None, self.restore_execution)
        self.assertEqual(self.restore_execution.state, 2)
