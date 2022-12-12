import os

from gb_module.gb_module.core.storage_module import StorageModule
from gb_module.gb_module.core.backup_result import BackupResult
from gb_module.gb_module.core.storage_result import StorageResult
from pathlib import Path
import shutil
import subprocess

class GBModule(StorageModule):
    def create_private_key_file(self, private_key, temp_folder):
        private_key_path = None
        if private_key:
            self.log(f"create private_key file ...")
            # add a \n at the end if not \n is at the end (is needed for a lot of ssh commands)
            if not private_key.endswith("\n"):
                private_key += "\n"
            # replace \r\n with \n because scp can't handle it otherwise
            private_key = private_key.replace("\r\n", "\n")
            private_key_path = str(Path(temp_folder).joinpath("private_key"))
            with open(private_key_path, "w") as file:
                file.write(private_key)
            os.chmod(private_key_path, 0o600)
        return private_key, private_key_path

    def save_to_storage(self, backup_result: BackupResult):
        # check if we have a path
        self.log(f"check inputs ...")
        path = self.get_param_with_name('path')
        if not path:
            return StorageResult.with_error("No path was provided!")

        port = str(self.get_param_with_name('port') or 22)
        private_key = self.get_secret_with_name('private_key')
        private_key_path = None
        username = self.get_param_with_name('username')
        host = self.get_param_with_name('host')
        self.log(f"host: {host}")
        backup_file_location = backup_result.backup_temp_location
        backup_file_name = self.get_backup_file_name("backup")
        backup_file_path = str(Path(path).joinpath(backup_file_name))

        self.log(f"backup_file_path {backup_file_location}")
        self.log("create temp folder ...")
        temp_folder = self.get_temp_folder_path("scp_module")
        os.mkdir(temp_folder)

        if not username:
            return StorageResult.with_error("No username was provided!")

        if not host:
            return StorageResult.with_error("No host was provided from system!")


        private_key, private_key_path = self.create_private_key_file(private_key, temp_folder)

        if not backup_file_location:
            self.log(f"create backup temp file ...")
            if not backup_result.raw_backup:
                return StorageResult.with_error("No raw backup or temp_location file provided!")
            backup_file_location = str(Path(temp_folder).joinpath("backup_file"))
            with open(backup_file_location, "w") as file:
                file.write(backup_result.raw_backup)

        scp_command = ['scp', '-o', 'StrictHostKeyChecking no', '-q', '-P', port]
        if private_key_path:
            scp_command += ['-i', private_key_path]

        scp_command += [backup_file_location, f"{username}@{host}:{backup_file_path}"]
        error = None
        result = None
        try:
            self.log(f"run {' '.join(scp_command)}")
            result = subprocess.run(scp_command, capture_output=True, input=b"yes")
        except Exception as exception:
            self.log(f"error at storing process: {exception}")
            error = f"error at scp command: {exception}"

        if result and result.stderr:
            error = f"error at storing process on server: {result.stderr.decode()}"

        self.log("cleanup created folders and files ...")
        #shutil.rmtree(temp_folder, ignore_errors=True)

        if error:
            return StorageResult.with_error(error)

        # return the StorageResult
        self.log(f"backup was successful")
        return StorageResult(path=f"{backup_file_path}",
                             output="Backup successfully stored"
                             )
