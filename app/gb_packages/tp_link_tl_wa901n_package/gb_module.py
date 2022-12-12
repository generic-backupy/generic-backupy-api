from pathlib import Path

from gb_module.gb_module.core.backup_module import BackupModule
from gb_module.gb_module.core.backup_result import BackupResult
import os
import shutil

from gb_packages.tp_link_tl_wa901n_package.utils.backup_fetcher import BackupFetcher


class GBModule(BackupModule):

    def do_backup(self):
        # check secrets and params
        self.log("check secrets and params ...")
        password = self.get_input_with_name("password")
        if not password:
            return BackupResult.with_error("No password in secrets")
        host = self.get_input_with_name("host")
        if not host:
            return BackupResult.with_error("No host in parameters")
        ap_type = self.get_param_with_name("ap_type") or "TL-WA901N"

        # create temp_folder
        self.log("create temp folder ...")
        temp_folder = self.get_temp_folder_path(ap_type)
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder, ignore_errors=True)
        os.mkdir(temp_folder)

        self.log("do backup ...")
        try:
            BackupFetcher.fetch_backup(temp_folder, host, password)
        except Exception as e:
            return BackupResult.with_error(f"Error at fetching: {e}", delete_path=temp_folder)

        # check the backup and return
        self.log("check backup")
        file_path = None
        listdir = os.listdir(temp_folder)
        if len(listdir) > 0:
            file_path = str(Path(temp_folder).joinpath(listdir[0]))
        if not os.path.exists(file_path):
            return BackupResult.with_error("Error at download process!", delete_path=temp_folder)

        self.log("backup was successful")
        return BackupResult(backup_temp_location=file_path, delete_path=temp_folder)
