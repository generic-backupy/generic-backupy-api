from pathlib import Path

from gb_module.gb_module.core.backup_module import BackupModule
from gb_module.gb_module.core.backup_result import BackupResult
import hmac
import os

from gb_packages.gs116ev2_switch_package.utils.backup_fetcher import BackupFetcher


class GBModule(BackupModule):

    def do_backup(self):
        # check secrets and params
        self.log("check secrets and params ...")
        try:
            password = self.get_input_with_name_or_die("password")
            host = self.get_input_with_name_or_die("host")
            protocol = self.get_input_with_name("protocol") or "http"
            timeout = self.get_input_with_name("timeout") or 60
            switch_type = self.get_input_with_name("switch_type") or "GS116Ev2"
            login_input_id = self.get_input_with_name("login_input_id") or "passwordtmp"
            login_button_id = self.get_input_with_name("login_button_id") or "btnApply"
            backup_endpoint = self.get_input_with_name("backup_endpoint") or f"{switch_type}.cfg"
            if backup_endpoint.startswith("/"):
                backup_endpoint = backup_endpoint[1:]
        except Exception as e:
            return BackupResult.with_error(f"input-error: {e}")

        # create temp_folder
        self.log("create temp folder ...")
        try:
            temp_folder = self.create_temp_folder(switch_type)
        except Exception as e:
            return BackupResult.with_error(f"temp-folder-creation-error: {e}")

        # do the backup
        self.log("do backup ...")
        try:
            BackupFetcher.fetch_backup(temp_folder, host, password, switch_type,
                                       login_input_id, login_button_id,
                                       backup_endpoint, protocol=protocol,
                                       timeout=timeout
                                       )
        except Exception as e:
            return BackupResult.with_error(f"Error at fetching: {e}", delete_path=temp_folder)

        # check the backup and return
        self.log("check backup")
        try:
            file_path = self.get_file_path_in_folder(temp_folder, f"{switch_type}.cfg")
        except Exception as e:
            return BackupResult.with_error(f"Error at checking file-path: {e}", delete_path=temp_folder)
        if not os.path.exists(file_path):
            return BackupResult.with_error("Error at download process!", delete_path=temp_folder)

        self.log(f"backup was successful, and is stored with temp path {file_path}")
        return BackupResult(backup_temp_location=file_path, delete_path=temp_folder)

    """
    python representation of the javascript function on the target switch (if we want to switch to requests in the future)
    currently it is not possible, because the switch doesn't support multi-tcp-segments for a HTTP Request (weird)
    """
    def calc_md5_pw(self, password):
        count = 0
        space = "\0"
        md5_key = "YOU_CAN_NOT_PASS"
        passwrd = ""
        while count <= (2048 - (len(password) + 1)):
            if count == 0:
                passwrd = password
            else:
                passwrd += password
            passwrd += space
            count += (len(password)+1)
        while count < 2048:
            passwrd += space
            count += 1
        return hmac.new(md5_key.encode(), msg=passwrd.encode(), digestmod="md5").hexdigest()
