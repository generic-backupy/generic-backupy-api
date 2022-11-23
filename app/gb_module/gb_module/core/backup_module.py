from .base_module import BaseModule
from .backup_result import BackupResult

class BackupModule(BaseModule):

    def __init__(self):
        super().__init__()

    def do_backup(self):
        pass

    def do_restore(self, backup):
        pass
