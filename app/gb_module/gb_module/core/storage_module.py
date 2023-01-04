from .base_module import BaseModule
from .backup_result import *

class StorageModule(BaseModule):

    def __init__(self):
        super().__init__()
        self.encryption_secret = {}
        self.retrieve_path = None

    def save_to_storage(self, backup_result: BackupResult):
        pass

    def retrieve_from_storage(self):
        pass
