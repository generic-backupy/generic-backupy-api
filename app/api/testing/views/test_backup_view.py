from unittest.mock import patch, Mock

from api.models import Category, Backup
from api.testing.test_utils.backup_job_test_util import BackupJobTestUtil
from api.testing.test_utils.category_test_util import CategoryTestUtil
from api.utils.backup_util import BackupUtil

from api.views.base_view import UserCurrentConditionsPermission

from api.views import BaseViewSet, CategoryViewSet, BackupViewSet
from django.test import TestCase


class BackupViewSetTest(TestCase):

    def setUp(self):
        self.view = BackupViewSet()
        self.job_switch_1, self.job_switch_2, \
        self.job_access_point, self.job_special_switch_2 = BackupJobTestUtil.create_network_test_backup_jobs()
        self.backup_1 = Backup.objects.create(name="TestBackup")

    @patch.object(BackupUtil, 'do_restore')
    def test_all_category(self, mock_do_restore):
        self.view.get_object = Mock(return_value=self.backup_1)
        request = Mock(user=None)
        self.view.request = request
        self.view.execute_restore(request)
        self.assertEqual(mock_do_restore.call_count, 1, "Call do_restore")
