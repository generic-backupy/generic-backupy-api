from .base_module import BaseModule


class StorageModule(BaseModule):

    def __init__(self):
        super().__init__()

    def save_to_storage(self, backup):
        pass

    def retrieve_from_storage(self):
        pass
