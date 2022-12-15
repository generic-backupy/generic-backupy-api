from unittest.mock import patch, Mock

from api.models import Category
from api.testing.test_utils.category_test_util import CategoryTestUtil
from api.utils.category_util import CategoryUtil

from api.views.base_view import UserCurrentConditionsPermission

from api.views import BaseViewSet, CategoryViewSet
from django.test import TestCase
from api.utils.ExecutionUtil import ExecutionUtil


class TestCategoryUtil(TestCase):

    def test_waiting(self):
        self.assertEqual(ExecutionUtil.get_state_string(0), "waiting")

    def test_running(self):
        self.assertEqual(ExecutionUtil.get_state_string(1), "running")

    def test_error(self):
        self.assertEqual(ExecutionUtil.get_state_string(2), "error")

    def test_success(self):
        self.assertEqual(ExecutionUtil.get_state_string(3), "success")
