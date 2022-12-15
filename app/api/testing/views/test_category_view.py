from unittest.mock import patch, Mock

from api.models import Category
from api.testing.test_utils.backup_job_test_util import BackupJobTestUtil
from api.testing.test_utils.category_test_util import CategoryTestUtil
from api.utils.backup_util import BackupUtil

from api.views.base_view import UserCurrentConditionsPermission

from api.views import BaseViewSet, CategoryViewSet
from django.test import TestCase


class CategoryViewSetTest(TestCase):

    def setUp(self):
        self.view = CategoryViewSet()
        self.job_switch_1, self.job_switch_2, \
        self.job_access_point, self.job_special_switch_2 = BackupJobTestUtil.create_network_test_backup_jobs()

    @patch.object(BackupUtil, 'do_backup')
    def test_all_category(self, mock_do_backup):
        self.view.get_object = Mock(return_value=Category.objects.filter(name="all").first())
        request = Mock(user=None)
        self.view.request = request
        self.view.execute_backup(request)
        self.assertEqual(mock_do_backup.call_count, 4, "Should include all jobs")


    @patch.object(BackupUtil, 'do_backup')
    def test_model_class(self, mock_do_backup):
        self.view.get_object = Mock(return_value=Category.objects.filter(name="switch").first())
        request = Mock(user=None)
        self.view.request = request
        self.view.execute_backup(request)
        self.assertEqual(mock_do_backup.call_count, 3, "Should include switches and special switch job")


    @patch.object(BackupUtil, 'do_backup')
    def test_model_class(self, mock_do_backup):
        self.view.get_object = Mock(return_value=Category.objects.filter(name="access point").first())
        request = Mock(user=None)
        self.view.request = request
        self.view.execute_backup(request)
        self.assertEqual(mock_do_backup.call_count, 1, "Should include only access point job")
