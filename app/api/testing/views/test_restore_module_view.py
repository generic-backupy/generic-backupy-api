from unittest.mock import patch, Mock

from api.models import Category, Backup
from api.rq_tasks.module_installation import install_module
from api.testing.test_utils.backup_job_test_util import BackupJobTestUtil
from api.testing.test_utils.category_test_util import CategoryTestUtil
from api.utils.backup_util import BackupUtil

from api.views.base_view import UserCurrentConditionsPermission

from api.views import BaseViewSet, CategoryViewSet, BackupViewSet, StorageModuleViewSet
from django.test import TestCase


class StorageModuleViewSetTest(TestCase):

    def setUp(self):
        self.view = StorageModuleViewSet()
        self.job_switch_1, self.job_switch_2, \
        self.job_access_point, self.job_special_switch_2 = BackupJobTestUtil.create_network_test_backup_jobs()
        self.backup_1 = Backup.objects.create(name="TestBackup")

    @patch('api.rq_tasks.module_installation')
    def test_no_content_type(self, mock_module_installation):
        with open("api/testing/test_files/module.zip", "r") as fp:
            request = Mock(user=None, FILES={"file_uploaded": fp})
            mock_module_installation.delay = Mock()
            self.view.request = request
            self.view.create(request)
            self.assertEqual(mock_module_installation.delay.call_count, 0, "Call module_installation")
