from gb_module.gb_module.core.storage_module import StorageModule
from gb_module.gb_module.core.backup_result import BackupResult
from gb_module.gb_module.core.storage_result import StorageResult
from pathlib import Path
import shutil

class GBModule(StorageModule):
    def save_to_storage(self, backup_result: BackupResult):
        # check if we have a path
        self.log(f"check path ...")
        path = self.get_param_with_name('path')
        if not path:
            return StorageResult.with_error("No path was provided!")

        # create file name and full path for that file
        self.log(f"create paths ...")
        path = Path(path)
        backup_file_name = self.get_backup_file_name()
        full_path = Path(path.absolute()).joinpath(backup_file_name)

        # save raw_backup to file
        if backup_result.raw_backup:
            self.log(f"save raw backup to {full_path.absolute()} ...")
            try:
                with open(full_path.absolute(), 'w') as file:
                    file.write(backup_result.raw_backup)
            except Exception as exception:
                self.log(f"error at storing process: {exception}")
                return StorageResult.with_error(f"error at storing process: {exception}")
        else: # use the temporal saved file (for big files) and copy it to the destination
            self.log(f"save temp file from {backup_result.backup_temp_location} to {full_path.absolute()} ...")
            try:
                shutil.copyfile(backup_result.backup_temp_location, full_path.absolute())
            except Exception as exception:
                self.log(f"error at storing process: {exception}")
                return StorageResult.with_error(f"error at storing process: {exception}")

        # return the StorageResult
        self.log(f"backup was successful")
        return StorageResult(path=f"{full_path.absolute()}",
                             output="Backup successfully stored"
                             )
