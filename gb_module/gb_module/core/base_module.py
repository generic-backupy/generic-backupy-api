from datetime import datetime
import re
import os
from pathlib import Path
import shutil


class BaseModule:

    def __init__(self, temp_path="/opt/backup_temp"):
        self.secrets = {}
        self.parameters = {}
        self.log = BaseModule.default_log
        self.system = {}
        self.backup_job = {}
        self.temp_path = None
        self.set_temp_path(temp_path)

    """
    sets the temp path for temp files, and creates it if it doesn't exists
    """

    def set_temp_path(self, path):
        self.temp_path = path
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)

    @staticmethod
    def default_log(message):
        print(message)

        """
    Returns the secret with a given name, if it exists.
    Otherwise it returns None
    """

    def get_secret_with_name(self, secret_name):
        if not self.secrets:
            return None
        return self.secrets.get(secret_name)

    """
    Returns the parameter with a given name, if it exists.
    Otherwise it returns None
    """

    def get_param_with_name(self, param_name):
        if not self.parameters:
            return None
        return self.parameters.get(param_name)

    """
    Returns a input with a given name, if it exists.
    A input will be fetched of all params, secrets, and system properties (like host)
    params overrides system, and secrets overrides system and params
    Otherwise it returns None
    """

    def get_input_with_name(self, param_name):
        # fetch from system
        value = (self.system or {}).get(param_name)
        # or params
        value = self.get_param_with_name(param_name) or value
        # or secrets
        value = self.get_secret_with_name(param_name) or value

        return value

    """
   Returns the input, or raise an exception, if the input isn't available
   """

    def get_input_with_name_or_die(self, param_name):
        value = self.get_input_with_name(param_name)
        if not value:
            raise Exception(f"{param_name} not specified!")
        return value

    """
    Returns a current datetime string with a format
    """

    def get_current_datetime_str(self, date_time=None, dt_format="%y_%m_%d__%H_%M_%S_%f"):
        return (date_time or datetime.now()).strftime(dt_format)

    """
    normalize a name to get a valid file_name out of it
    TODO: remove not allowed characters
    """

    def get_normalized_name(self, name: str):
        name = name.replace(" ", "_")
        name = name.lower()
        return name

    """
    normalize a name to get a valid file_name out of it
    TODO: remove not allowed characters
    """

    def get_backup_file_name(self, name=None, suffix=".bk"):
        backup_name = f"{name or self.backup_job.get('name')}_{self.get_current_datetime_str()}{suffix}"
        backup_name = backup_name.replace(" ", "_")
        backup_name = re.sub('(?<!^)(?=[A-Z])', '_', backup_name).lower()
        return backup_name

    """
    generate a temp_folder name with datetime and url normalized string
    """

    def get_temp_folder_name(self, name=None):
        folder = f"{name}_temp_{self.get_current_datetime_str()}"
        folder = folder.replace(" ", "_")
        folder = re.sub('(?<!^)(?=[A-Z])', '_', folder).lower()
        return folder

    """
    get the whole path to a the current temp folder (which is in the default temp_path
    """

    def get_temp_folder_path(self, name=None):
        return str(Path(self.temp_path).joinpath(self.get_temp_folder_name(name)))

    """
    generate a tempfolder, with creating and cleaning up existing temp folders with the same name
    """

    def create_temp_folder(self, name):
        temp_folder = self.get_temp_folder_path(name)
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder, ignore_errors=True)
        os.mkdir(temp_folder)
        return temp_folder

    """
    check if a file is in the specified temp_folder (with file_name or any file)
    """

    def get_file_path_in_folder(self, temp_folder, file_name=None):
        file_path = None
        listdir = os.listdir(temp_folder)
        if len(listdir) > 0:
            if file_name and os.path.exists(Path(temp_folder).joinpath(file_name)):
                file_path = Path(temp_folder).joinpath(file_name)
            else:
                file_path = str(Path(temp_folder).joinpath(listdir[0]))

        return file_path

    """
    get the host
    """
    def get_host(self):
        return self.get_input_with_name("host")


    def write_raw_backup_to_temp_storage(self, raw_backup, temp_folder):
        self.log(f"create backup temp file ...")
        if not raw_backup:
            raise Exception("No raw backup or temp_location file provided!")
        backup_file_location = str(Path(temp_folder).joinpath("backup_file"))
        with open(backup_file_location, "w") as file:
            file.write(raw_backup)
        return backup_file_location
