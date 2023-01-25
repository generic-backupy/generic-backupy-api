from .base_module import BaseModule
from .backup_result import BackupResult
from .retrieve_result import RetrieveResult


class BackupModule(BaseModule):

    def __init__(self, temp_path="/opt/backup_temp"):
        super().__init__(temp_path=temp_path)

    def do_backup(self):
        pass

    def do_restore(self, retrieve_result: RetrieveResult):
        pass
