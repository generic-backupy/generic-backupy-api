from datetime import datetime
import re

class BaseModule:

    def __init__(self):
        self.secrets = []
        self.parameters = []
        self.log = BaseModule.default_log
        self.system = {}
        self.backup_job = {}

    @staticmethod
    def default_log(message):
        print(message)

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
