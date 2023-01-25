from gb_module.core.backup_module import BackupModule
from gb_module.core.backup_result import BackupResult
import time

from gb_module.core.restore_result import RestoreResult
from gb_module.core.retrieve_result import RetrieveResult


class GBModule(BackupModule):
    def do_backup(self):
        # simulate long running backup process
        self.log("do backup ...")
        time.sleep(2)
        self.log("done ...")
        return BackupResult(output=f"backup was successfully", raw_backup="{'v': 1, 'type': 'fake_backup'}")

    def do_restore(self, retrieve_result: RetrieveResult):
        self.log("restore retrieved backup ...")
        if retrieve_result.raw_backup:
            self.log(f"restore raw_backup: {retrieve_result.raw_backup}")
        elif retrieve_result.backup_temp_location:
            self.log(f"restore backup_temp_location ...")
            with open(retrieve_result.backup_temp_location, "r") as f:
                self.log(f"loaded restore file: {f.readlines()}")
        else:
            self.log("no backup provided")
            return RestoreResult.with_error("no backup provided")

        return RestoreResult("backup successfully restored")
