from gb_module.gb_module.core.storage_module import StorageModule
from gb_module.gb_module.core.backup_result import BackupResult
from gb_module.gb_module.core.storage_result import StorageResult
import time

class GBModule(StorageModule):
    def save_to_storage(self, backup_result: BackupResult):
        # simulate long running storing process
        self.log("start storing process (mock)")
        self.log("connect to server ...")
        time.sleep(2)
        self.log("copy to server ...")
        time.sleep(3)
        self.log("take the final steps ...")
        time.sleep(2)
        self.log("done ...")
        return StorageResult(path="/backup/test/test.bk",
                             additional_parameters_dict={"token": "dfdfdf"},
                             output="Backup successfully stored"
                             )
