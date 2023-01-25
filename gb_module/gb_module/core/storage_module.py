from pathlib import Path

from .base_module import BaseModule
from .backup_result import *

class StorageModule(BaseModule):

    def __init__(self, temp_path="/opt/backup_temp"):
        super().__init__(temp_path=temp_path)
        self.encryption_secret = {}
        self.retrieve_path = None

    def save_to_storage(self, backup_result: BackupResult):
        pass

    def retrieve_from_storage(self):
        pass

    def get_target_retrieved_file_name(self, temp_folder):
        return Path(temp_folder).joinpath(self.get_input_with_name('original_backup_name') or 'backup_file')

