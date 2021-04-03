from django.db import models
from django.conf import settings
from django.utils.translation import get_language as get_language

class BaseModel(models.Model):

    @staticmethod
    def on_delete_if_creator_will_deleted():
        return models.CASCADE

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)
    created_language = models.CharField(max_length=10, default="en")

    # Filter
    search_fields = []
    ordering_fields = []
    ordering = []
    filterset_fields = []

    initial_model = {}

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self.initial_model = self.__dict__.copy()

    class Meta:
        abstract = True

    def set_deleted(self):
        self.deleted = True

    def save(self, *args, **kwargs):
        # add the language code at creation or update
        lang = get_language()
        if lang:
            self.created_language = get_language()
        super(BaseModel, self).save(*args, **kwargs)
