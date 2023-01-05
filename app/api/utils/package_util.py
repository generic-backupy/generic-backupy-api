import importlib.util
import sys

from api.serializers import SystemGbModuleSerializer, SecretGbModuleSerializer
from api.utils.backup_job_util import BackupJobUtil
from gb_module.gb_module.core.base_module import BaseModule

from api.exceptions import AppErrorException
from api.models import BackupModule, BackupJob, BackupJobStorageModule
from django.utils.timezone import now

from gb_module.gb_module.core.base_result import BaseResult


class PackageUtil:

    """
    returns True if there was an error, and handle the execution_instance stuff
    """
    @staticmethod
    def handle_error_if_exist(module_response, execution_instance):
        has_error = False
        if not module_response or module_response.error:
            has_error = True
            execution_instance.state = 2
            if module_response:
                execution_instance.errors = (execution_instance.errors or "") + (module_response.error or "")
            elif not execution_instance.errors:
                execution_instance.errors = "UNKNOWN ERROR"
        if module_response:
            execution_instance.output = module_response.output
        execution_instance.save()

        return has_error
    
    @staticmethod
    def inject_storage_parameters(package_instance: BaseModule, backup_job: BackupJob, storage_module_pivot: BackupJobStorageModule, additional_parameters={}):
        # inject the secrets
        package_instance.secrets = BackupJobUtil.parsed_storage_secret_dict(storage_module_pivot)
        # inject the params
        package_instance.parameters = BackupJobUtil.parsed_storage_parameter_dict(storage_module_pivot)
        # inject direct params
        package_instance.parameters |= (storage_module_pivot.direct_parameters or {}) | additional_parameters
        # inject the system
        package_instance.system = SystemGbModuleSerializer(backup_job.system).data

        # inject encryption_secret if specified
        if storage_module_pivot.encryption_secret:
            package_instance.encryption_secret = SecretGbModuleSerializer(
                storage_module_pivot.encryption_secret).data
    
    @staticmethod
    def inject_backup_parameters(package_instance: BaseModule, backup_job: BackupJob, additional_parameters={}):
        # inject the secrets
        package_instance.secrets = BackupJobUtil.parsed_secret_dict(backup_job)
        # inject the params
        package_instance.parameters = BackupJobUtil.parsed_parameter_dict(backup_job)
        # inject direct params
        package_instance.parameters |= (backup_job.backup_module_direct_parameters or {}) | additional_parameters
        # inject the system
        package_instance.system = SystemGbModuleSerializer(backup_job.system).data

    @staticmethod
    def inject_module_log_function(package_instance: BaseModule, execution_instance):
        # inject the log function
        def backup_log(message):
            message = f"{now()} - {message}\n"
            print(message)
            if not execution_instance.logs:
                execution_instance.logs = message
            else:
                execution_instance.logs += message
            execution_instance.save()
        package_instance.log = backup_log

    @staticmethod
    def get_package_instance_or_error(execution_instance, module_instance):
        package_instance = None
        # get an instance of the plugin
        try:
            package_instance = PackageUtil.get_python_class_of_module(module_instance)()
        except FileNotFoundError as e:
            print("file not found error at loading backup_instance")
            execution_instance.errors = f"file not found error: {e}"
        except Exception as e:
            print("error at loading backup_instance")
            execution_instance.errors = f"file not found error: {e}"

        if not package_instance:
            execution_instance.save()
            return

        return package_instance

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
