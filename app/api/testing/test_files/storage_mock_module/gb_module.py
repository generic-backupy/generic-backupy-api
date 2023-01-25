from gb_module.core.retrieve_result import RetrieveResult
from gb_module.core.storage_module import StorageModule
from gb_module.core.backup_result import BackupResult
from gb_module.core.storage_result import StorageResult
from pathlib import Path
import subprocess


class GBModule(StorageModule):
    def save_to_storage(self, backup_result: BackupResult):
        self.log("create temp folder ...")
        try:
            temp_folder = self.create_temp_folder("mock_module")
        except Exception as e:
            return BackupResult.with_error(f"temp-folder-creation-error: {e}")

        backup_file_location = backup_result.backup_temp_location
        backup_file_name = self.get_backup_file_name("backup")
        backup_file_path = str(Path(temp_folder).joinpath(backup_file_name))

        if not backup_file_location:
            try:
                backup_file_location = self.write_raw_backup_to_temp_storage(backup_result.raw_backup, temp_folder)
            except Exception as e:
                return StorageResult.with_error(f"error at backup file creation (out of raw_backup): {e}")

        result = None
        error = None
        try:
            result = subprocess.run(['cp', backup_file_location, backup_file_path], capture_output=True, input=b"yes")
        except Exception as exception:
            self.log(f"error at storing process: {exception}")
            error = f"error at storing process: {exception}"

        if result and result.stderr:
            error = f"error at storing process after success: {result.stderr.decode()}"

        self.log("cleanup created folders and files ...")

        if error:
            return StorageResult.with_error(error)

        # return the StorageResult
        self.log(f"store process was successful")
        return StorageResult(path=f"{backup_file_path}",
                             output="Backup successfully stored"
                             )

    def retrieve_from_storage(self):
        if not self.retrieve_path:
            return BackupResult.with_error(f"no retrieve path (path on the remote server)")

        # create temp_folder
        self.log("create temp folder ...")
        try:
            temp_folder = self.create_temp_folder("scp_module")
        except Exception as e:
            return BackupResult.with_error(f"temp-folder-creation-error: {e}")

        error = None
        result = None
        retrieve_temp_path = self.get_target_retrieved_file_name(temp_folder)
        try:
            result = subprocess.run(["cp", self.retrieve_path, retrieve_temp_path], capture_output=True, input=b"yes")
        except Exception as exception:
            self.log(f"error at storing process: {exception}")
            error = f"error at scp command: {exception}"

        if result and result.stderr:
            error = f"error at storing process on server: {result.stderr.decode()}"

        self.log("cleanup created folders and files ...")

        if error:
            return StorageResult.with_error(error)

        # return the StorageResult
        self.log(f"backup was successful")
        return RetrieveResult(backup_temp_location=f"{retrieve_temp_path}", output="Backup successfully retrieved", delete_path=f"{temp_folder}")
