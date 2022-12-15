from unittest.mock import patch, Mock

from api.models import Category
from api.testing.test_utils.category_test_util import CategoryTestUtil
from api.utils.category_util import CategoryUtil

from api.views.base_view import UserCurrentConditionsPermission

from api.views import BaseViewSet, CategoryViewSet
from django.test import TestCase


class TestCategoryUtil(TestCase):

    def setUp(self):
        self.all, \
        self.network, \
        self.switch, \
        self.access_point, \
        self.special_switch \
            = CategoryTestUtil.create_network_test_categories()

    def test_get_child_categories_all(self):
        categories = CategoryUtil.get_child_categories(self.all)
        self.assertListEqual(categories, [self.all, self.network, self.switch, self.special_switch, self.access_point])
