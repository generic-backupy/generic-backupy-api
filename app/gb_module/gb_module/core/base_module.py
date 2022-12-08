from datetime import datetime
import re
import os
from pathlib import Path


class BaseModule:

    def __init__(self):
        self.secrets = []
        self.parameters = []
        self.log = BaseModule.default_log
        self.system = {}
        self.backup_job = {}
        self.temp_path = None
        self.set_temp_path("/opt/backup_temp")

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
        # reverse loop because the last parameters overrides the first ones (if there are the same)
        for secret_obj in reversed(self.secrets):
            if type(secret_obj).__name__ == 'dict':
                secret = secret_obj.get('secret') or {}
                if secret_name == secret_obj.get('key'):
                    return secret
        return None

    """
    Returns the parameter with a given name, if it exists.
    Otherwise it returns None
    """
    def get_param_with_name(self, param_name):
        if not self.parameters:
            return None
        # reverse loop because the last parameters overrides the first ones (if there are the same)
        for param_obj in reversed(self.parameters):
            if type(param_obj).__name__ == 'dict':
                parameter = param_obj.get('parameter') or {}
                if param_name in parameter:
                    return parameter.get(param_name)
        return None

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
    def get_backup_file_name(self, name=None):
        backup_name = f"{name or self.backup_job.get('name')}_{self.get_current_datetime_str()}.bk"
        backup_name = backup_name.replace(" ", "_")
        backup_name = re.sub('(?<!^)(?=[A-Z])', '_', backup_name).lower()
        return backup_name


    def get_temp_folder_name(self, name=None):
        folder = f"{name}_temp_{self.get_current_datetime_str()}"
        folder = folder.replace(" ", "_")
        folder = re.sub('(?<!^)(?=[A-Z])', '_', folder).lower()
        return folder


    def get_temp_folder_path(self, name=None):
        return str(Path(self.temp_path).joinpath(self.get_temp_folder_name(name)))
