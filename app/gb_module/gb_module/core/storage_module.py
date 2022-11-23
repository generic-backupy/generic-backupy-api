from .base_module import BaseModule
from .backup_result import *

class StorageModule(BaseModule):

    def __init__(self):
        super().__init__()

    def save_to_storage(self, backup_result: BackupResult):
        pass

    def retrieve_from_storage(self):
        pass
