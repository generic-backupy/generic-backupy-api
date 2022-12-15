from api.models import Category, System
from api.testing.test_utils.category_test_util import CategoryTestUtil


class SystemTestUtil:

    @staticmethod
    def create_network_test_categories():
        all, \
        network, \
        switch, \
        access_point, \
        special_switch \
            = CategoryTestUtil.create_network_test_categories()

        switch_1 = System.objects.create(name="switch 1", host="0.0.0.0", category=switch)
        switch_2 = System.objects.create(name="switch 2", host="0.0.0.1", category=switch)
        special_switch_1 = System.objects.create(name="special switch 1", host="0.0.1.1", category=special_switch)
        access_point_1 = System.objects.create(name="acces_point_1 1", host="0.0.0.2", category=access_point)

        return switch_1, switch_2, access_point_1, special_switch_1
