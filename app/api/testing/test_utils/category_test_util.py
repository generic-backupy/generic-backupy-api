from api.models import Category


class CategoryTestUtil:

    @staticmethod
    def create_network_test_categories():
        all = Category.objects.create(name="all")
        network = Category.objects.create(name="network", parent=all)
        switch = Category.objects.create(name="switch", parent=network)
        access_point = Category.objects.create(name="access point", parent=network)
        special_switch = Category.objects.create(name="special switch", parent=switch)

        return all, network, switch, access_point, special_switch
