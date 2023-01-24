import datetime
from unittest.mock import patch, Mock

from api.testing.test_utils.backup_job_test_util import BackupJobTestUtil

from api.models import Backup, RestoreExecution, BackupModule, StorageModule, \
    BackupJobStorageModule, BackupExecution, BackupSchedule, User
from api.testing.test_utils.module_test_util import ModuleTestUtil
from api.utils.backup_util import BackupUtil
from api.utils.package_util import PackageUtil
from django.test import TestCase
from gb_module.gb_module.core.base_result import BaseResult
from api.rq_tasks.restore import restore
from api.rq_tasks.backup import backup
from api.rq_tasks.schedule_backup import schedule

class TestRestore(TestCase):

    def setUp(self) -> None:
        self.restore_execution = RestoreExecution.objects.create()

        self.job_switch_1, self.job_switch_2, self.job_access_point, self.job_special_switch_2 = BackupJobTestUtil.create_network_test_backup_jobs()
        self.backup_schedule = BackupSchedule.objects.create(name="test", backup_job=self.job_switch_1, next_start=datetime.datetime.now())
        self.user = User.objects.create_user("test")

    @patch.object(BackupUtil, 'do_backup')
    def test_schedule_refresh_next_time(self, mock_do_backup):
        old_time = self.backup_schedule.next_start
        schedule(self.backup_schedule.backup_job, self.user, self.backup_schedule)
        self.assertTrue(mock_do_backup.called, "do backup wasn't called")
        self.assertNotEqual(old_time, self.backup_schedule.next_start, "next_start wasn't extended")
        self.assertIsNotNone(self.backup_schedule.last_start, "last_start shouldn't be None")
        self.assertEqual(old_time, self.backup_schedule.last_start, "last_start wasn't set")
