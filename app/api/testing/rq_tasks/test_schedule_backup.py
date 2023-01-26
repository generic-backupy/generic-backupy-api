import datetime
from unittest.mock import patch, Mock

from api.testing.test_utils.backup_job_test_util import BackupJobTestUtil

from api.models import RestoreExecution, User
from api.utils.backup_util import BackupUtil
from django.test import TestCase
from api.rq_tasks.schedule_backup import schedule
from api.models.backup_schedule import BackupSchedule

class TestRestore(TestCase):

    def setUp(self) -> None:
        self.mock_enqeue_at = Mock()
        self.mock_enqeue_at.enqueue_at = Mock(return_value=Mock(id="mock_id"))
        self.mock_get_queue = Mock(return_value=self.mock_enqeue_at)
        BackupSchedule.get_queue = self.mock_get_queue
        self.restore_execution = RestoreExecution.objects.create()
        self.job_switch_1, self.job_switch_2, self.job_access_point, self.job_special_switch_2 = BackupJobTestUtil.create_network_test_backup_jobs()
        self.backup_schedule = BackupSchedule.objects.create(name="test", backup_job=self.job_switch_1, next_start=datetime.datetime.now())
        self.user = User.objects.create_user("test")

    @patch.object(BackupUtil, 'do_backup')
    def test_schedule_refresh_next_time(self, mock_do_backup):
        old_time = self.backup_schedule.next_start
        schedule(self.backup_schedule)
        self.assertTrue(mock_do_backup.called, "do backup wasn't called")
        self.assertNotEqual(old_time.timestamp(), self.backup_schedule.next_start.timestamp(), "next_start wasn't extended")
        self.assertIsNotNone(self.backup_schedule.last_start, "last_start shouldn't be None")
        self.assertEqual(old_time.timestamp(), self.backup_schedule.last_start.timestamp(), "last_start wasn't set")
        self.assertTrue(self.mock_enqeue_at.enqueue_at.called, "enqueu_at wasn't called")
