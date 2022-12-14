from gb_module.gb_module.core.backup_module import BackupModule
from gb_module.gb_module.core.backup_result import BackupResult
import os
from gb_packages.tp_link_tl_wa901n_package.utils.backup_fetcher import BackupFetcher


class GBModule(BackupModule):

    def do_backup(self):
        # check secrets and params
        self.log("check secrets and params ...")
        try:
            password = self.get_input_with_name_or_die("password")
            host = self.get_input_with_name_or_die("host")
            ap_type = self.get_input_with_name("ap_type") or "TL-WA901N"
        except Exception as e:
            return BackupResult.with_error(f"input-error: {e}")

        self.log("create temp folder ...")
        try:
            temp_folder = self.create_temp_folder(ap_type)
        except Exception as e:
            return BackupResult.with_error(f"temp-folder-creation-error: {e}")

        self.log("do backup ...")
        try:
            BackupFetcher.fetch_backup(temp_folder, host, password)
        except Exception as e:
            return BackupResult.with_error(f"Error at fetching: {e}", delete_path=temp_folder)

        # check the backup and return
        self.log("check backup")
        try:
            file_path = self.get_file_path_in_folder(temp_folder)
        except Exception as e:
            return BackupResult.with_error(f"Error at checking file-path: {e}", delete_path=temp_folder)
        if not os.path.exists(file_path):
            return BackupResult.with_error("Error at download process!", delete_path=temp_folder)

        self.log("backup was successful")
        return BackupResult(backup_temp_location=file_path, delete_path=temp_folder)
