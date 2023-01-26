from pathlib import Path

from gb_module.core.backup_module import BackupModule
from gb_module.core.backup_result import BackupResult
import time

from gb_module.core.restore_result import RestoreResult
from gb_module.core.retrieve_result import RetrieveResult
import os
import subprocess

class GBModule(BackupModule):

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

    def create_private_key(self, private_key, temp_folder):
        self.log("create private key ...")
        try:
            private_key, private_key_path = self.create_private_key_file(private_key, temp_folder)
        except Exception as e:
            return BackupResult.with_error(f"private key creation error: {e}")

    def create_inventory(self, temp_folder, inventory):
        self.log("create inventory ...")
        try:
            with open(Path(temp_folder).joinpath("inventory"), "w") as file:
                file.write(inventory.replace("{private_key_path}", str(Path(temp_folder).joinpath("private_key"))))
        except Exception as e:
            return BackupResult.with_error(f"inventory creation error: {e}")

    def create_playbook(self, temp_folder, playbook, file_path_placeholder, file_path):
        self.log("create playbook ...")
        try:
            with open(Path(temp_folder).joinpath("playbook"), "w") as file:
                file.write(playbook.replace(file_path_placeholder, file_path))
        except Exception as e:
            return BackupResult.with_error(f"playbook creation error: {e}")

    def do_backup(self):
        # check secrets and params
        self.log("check secrets and params ...")
        try:
            inventory = self.get_input_with_name_or_die("inventory")
            playbook = self.get_input_with_name_or_die("playbook")
            private_key = self.get_input_with_name_or_die("private_key")
        except Exception as e:
            return BackupResult.with_error(f"input-error: {e}")

        # create temp_folder
        self.log("create temp folder ...")
        try:
            temp_folder = self.create_temp_folder('ansible-module')
        except Exception as e:
            return BackupResult.with_error(f"temp-folder-creation-error: {e}")

        # create priv key
        error = self.create_private_key(private_key, temp_folder)
        if error:
            return error

        # create inventory {private_key_path}
        error = self.create_inventory(temp_folder, inventory)
        if error:
            return error

        # create playbook
        error = self.create_playbook(temp_folder, playbook, "{dest_file_path}", str(Path(temp_folder).joinpath("backup")))
        if error:
            return error

        # do the backup
        self.log("do backup ...")
        process_call = None
        #r = subprocess.run(["ls","dd"], capture_output=True, text=True)
        try:
            self.log(f"run ansible-playbook -i {Path(temp_folder).joinpath('inventory')} {Path(temp_folder).joinpath('playbook')} --ssh-common-args='-o StrictHostKeyChecking=no'")
            process_call = subprocess.run(["ansible-playbook", "-i", f"{Path(temp_folder).joinpath('inventory')}", f"{Path(temp_folder).joinpath('playbook')}", "--ssh-common-args='-o StrictHostKeyChecking=no'"], capture_output=True, text=True)
        except Exception as e:
            return BackupResult.with_error(f"Error at fetching: {e}", delete_path=temp_folder)

        if not process_call:
            return BackupResult.with_error(f"No output at process: ", delete_path=temp_folder)

        if process_call.stderr and len(process_call.stderr) > 0:
            return BackupResult.with_error(f"Error at fetching: {process_call.stderr}", delete_path=temp_folder)

        if process_call.stdout:
            self.log(f"output: {process_call.stdout}")

        # check the backup and return
        self.log("check backup")
        file_path = Path(temp_folder).joinpath("backup")
        if not file_path.exists():
            return BackupResult.with_error("Error at download process!", delete_path=temp_folder)

        self.log(f"backup was successful, and is stored with temp path {file_path}")
        return BackupResult(backup_temp_location=file_path, delete_path=temp_folder, original_backup_name=f"{Path(file_path).parts[-1]}")

    def do_restore(self, retrieve_result: RetrieveResult):
        if not retrieve_result.backup_temp_location:
            return BackupResult.with_error("no file to restore")
        # check secrets and params
        self.log("check secrets and params ...")
        try:
            inventory = self.get_input_with_name_or_die("inventory")
            inventory = self.get_input_with_name('inventory_restore') or inventory
            playbook = self.get_input_with_name_or_die("playbook")
            playbook = self.get_input_with_name('playbook_restore') or playbook
            private_key = self.get_input_with_name_or_die("private_key")
        except Exception as e:
            return BackupResult.with_error(f"input-error: {e}")

        # create temp_folder
        self.log("create temp folder ...")
        try:
            temp_folder = self.create_temp_folder('ansible-module')
        except Exception as e:
            return BackupResult.with_error(f"temp-folder-creation-error: {e}")

        # create priv key
        error = self.create_private_key(private_key, temp_folder)
        if error:
            return error

        # create inventory {private_key_path}
        error = self.create_inventory(temp_folder, inventory)
        if error:
            return error

        # create playbook
        self.log("create playbook ...")
        error = self.create_playbook(temp_folder, playbook, "{backup_file_path}", str(retrieve_result.backup_temp_location))
        if error:
            return error
        # do the backup
        self.log("do backup ...")
        process_call = None
        try:
            self.log(f"run ansible-playbook -i {Path(temp_folder).joinpath('inventory')} {Path(temp_folder).joinpath('playbook')} --ssh-common-args='-o StrictHostKeyChecking=no'")
            process_call = subprocess.run(["ansible-playbook", "-i", f"{Path(temp_folder).joinpath('inventory')}", f"{Path(temp_folder).joinpath('playbook')}", "--ssh-common-args='-o StrictHostKeyChecking=no'"], capture_output=True, text=True)
        except Exception as e:
            return BackupResult.with_error(f"Error at fetching: {e}", delete_path=temp_folder)

        if not process_call:
            return BackupResult.with_error(f"No output at process: ", delete_path=temp_folder)

        if process_call.stderr and len(process_call.stderr) > 0:
            return BackupResult.with_error(f"Error at fetching: {process_call.stderr}", delete_path=temp_folder)

        if process_call.stdout:
            self.log(f"output: {process_call.stdout}")

        return RestoreResult(output="restored")
