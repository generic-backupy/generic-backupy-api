from unittest.mock import patch, Mock

from api.models import Category, Backup, RestoreExecution
from api.rq_tasks.restore import restore
from api.testing.test_utils.category_test_util import CategoryTestUtil
from api.utils.backup_util import BackupUtil
from api.utils.category_util import CategoryUtil

from api.views.base_view import UserCurrentConditionsPermission

from api.views import BaseViewSet, CategoryViewSet
from django.test import TestCase
from api.utils.ExecutionUtil import ExecutionUtil


class TestBackupUtil(TestCase):

    def setUp(self) -> None:
        self.backup_1 = Backup.objects.create(name="Test")

    @patch("api.rq_tasks.restore.restore.delay")
    def test_call_restore_delay(self, mock_restore_delay_call):
        BackupUtil.do_restore(self.backup_1, None)
        self.assertEqual(mock_restore_delay_call.call_count, 1, "Call restore delay")

    @patch("api.rq_tasks.restore.restore.delay")
    def test_create_restore_execution(self, mock_restore_delay_call):
        amount_of_restore_executions = len(RestoreExecution.objects.all())
        BackupUtil.do_restore(self.backup_1, None)
        self.assertEqual(len(RestoreExecution.objects.all()) - 1, amount_of_restore_executions, "Exact 1 new restore execution should exist")
