import importlib.util
import sys

from api.exceptions import AppErrorException
from api.models import BackupModule


class PackageUtil:

    @staticmethod
    def get_python_class_of_module(backup_module: BackupModule):
        backup_class = None
        # TODO: change the GBModule to the name which is specified in the modules gb.json file.
        # TODO: also replace the python module file name
        module_name = "GBModule"
        module_file = "gb_module.py"
        file_system_path = backup_module.file_system_path
        # append a / if there is no / at the end
        file_system_path += "/" if not file_system_path.endswith("/") else ""
        # get the spec
        spec = importlib.util.spec_from_file_location(module_name, f"{file_system_path}{module_file}")
        if spec:
            python_module = importlib.util.module_from_spec(spec)
            if python_module:
                sys.modules[module_name] = python_module
                spec.loader.exec_module(python_module)
            backup_class = getattr(python_module, module_name)

        if not backup_class:
            raise AppErrorException("BackupModule Loading Error",
                                    "There was an error at the loading process of the backup module", status_code=400)

        return backup_class
