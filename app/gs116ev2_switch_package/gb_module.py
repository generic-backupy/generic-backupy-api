from pathlib import Path

from gb_module.gb_module.core.backup_module import BackupModule
from gb_module.gb_module.core.backup_result import BackupResult
import hmac
import os
import shutil

from gs116ev2_switch_package.utils.backup_fetcher import BackupFetcher


class GBModule(BackupModule):

    def do_backup(self):
        # check secrets and params
        self.log("check secrets and params ...")
        password = self.get_secret_with_name("password")
        if not password:
            self.log(f"secrets in module {self.secrets}")
            self.log(f"password {self.secrets[0].get('secret')}")
            self.log(f"key {self.secrets[0].get('key')}")
            self.log(f"type: {self.secrets[0].__name__}")
            return BackupResult.with_error("No password in secrets")
        host = self.get_param_with_name("host")
        if not host:
            return BackupResult.with_error("No host in parameters")

        # create temp_folder
        self.log("create temp folder ...")
        temp_folder = self.get_temp_folder_path("gs116ev2")
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder, ignore_errors=True)
        os.mkdir(temp_folder)

        # do the backup
        # TODO: outsource it to a function variable to have the opportunity to change the function to a mock alternative
        self.log("do backup ...")
        BackupFetcher.fetch_backup(temp_folder, host, password)

        # check the backup and return
        self.log("check backup")
        file_path = str(Path(temp_folder).joinpath("GS116Ev2.cfg"))
        if not os.path.exists(file_path):
            return BackupResult.with_error("Error at download process!", delete_path=temp_folder)

        self.log("backup was successful")
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
