from api.models import Category


class CategoryUtil:

    @staticmethod
    def get_child_categories(category: Category, visited_ids=None):
        if visited_ids is None:
            visited_ids = []
        categories = [category]
        visited_ids.append(category.id)
        for child in Category.objects.filter(parent=category):
            if child.id not in visited_ids:
                categories += CategoryUtil.get_child_categories(child, visited_ids)
        return categories
