from gb_module.gb_module.core.storage_module import StorageModule
from gb_module.gb_module.core.backup_result import BackupResult
from gb_module.gb_module.core.storage_result import StorageResult
import time
from pathlib import Path

class GBModule(StorageModule):
    def save_to_storage(self, backup_result: BackupResult):
        # check if we have a path
        path = self.get_param_with_name('path')
        if not path:
            return StorageResult.with_error("No path was provided!")

        # create file name and full path to that file
        path = Path(path)
        backup_file_name = self.get_backup_file_name()
        full_path = Path(path.absolute()).joinpath(backup_file_name)

        # save raw_backup to file
        if backup_result.raw_backup:
            try:
                with open(full_path.absolute(), 'w') as file:
                    file.write(backup_result.raw_backup)
            except Exception as exception:
                return StorageResult.with_error(f"error at storing process: {exception}")
        else:
            # TODO: implement datatransfer (blockwise if we need it to do per python code)
            pass

        return StorageResult(path=f"{full_path.absolute()}",
                             additional_parameters_dict={"token": "dfdfdf"},
                             output="Backup successfully stored"
                             )
