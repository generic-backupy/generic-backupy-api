from django_rq import job
from api.models import Backup, BackupModule, StorageModule, ModuleInstallationExecution
from django.utils.timezone import now
from api.utils.package_util import PackageUtil
from pathlib import Path
import os
import json

"""
install a module
module_type: 1=backup, 2=storage
"""
@job("default", timeout=60*30)
def install_module(filename, install_execution: ModuleInstallationExecution, module_type=1):
    install_execution.state = 1
    install_execution.logs = f"start installation ...\n"
    install_execution.save()
    path = Path("/packages").joinpath(filename)

    # unzip if it is a zip file
    if filename.endswith(".zip"):
        install_execution.log("try to unzip it ...")
        filename = filename.replace('.zip', '-unzipped')
        unzipped_path = Path("/packages").joinpath(filename)
        os.system(f"unzip {path} -d {unzipped_path}")
        os.system(f"rm -rf {path}")
        path = unzipped_path

        if not path.exists():
            install_execution.state = 2
            install_execution.log("unzip error")
            return

        # if there is only one folder in it, use this folder as the right one
        install_execution.log(f"listdir: {os.listdir(path)}, {len(os.listdir(path))}")
        if "gb.json" not in os.listdir(path):
            gbjson_found = True
            for dir in os.listdir(str(path)):
                cpath = Path(path).joinpath(dir)
                if cpath.is_dir():
                    if "gb.json" in os.listdir(cpath):
                        gbjson_found = True
                        install_execution.log(f"execute: mv {cpath}/* {path}")
                        os.system(f"mv \"{cpath}\"/* \"{path}\"")
                        os.system(f"rm -rf \"{cpath}\"")
                        break
            if not gbjson_found:
                install_execution.state = 2
                install_execution.log("no gb.json file found!")
                return

    # create the module object
    if module_type == 1:
        new_module = BackupModule(name="No name was specified", file_system_path=str(path))
    elif module_type == 2:
        new_module = StorageModule(name="No name was specified", file_system_path=str(path))
    else:
        install_execution.logs += f"wrong module type {module_type}!\n"
        install_execution.save()
        return

    # load config if exists, and save it to the model
    module_config_path = path.joinpath("gb.json")
    module_config = None
    if module_config_path.exists():
        try:
            with open(module_config_path, "r") as file:
                module_config = json.load(file)
                install_execution.logs += f"config loaded\n"
                install_execution.save()
                new_module.module_config = module_config
                new_module.name = module_config.get('module_name') or new_module.name
                new_module.description = module_config.get('module_description') or new_module.description
        except Exception as e:
            install_execution.logs += f"Config loading error: {e}\n"
            install_execution.save()

    # execute installation scripts
    if module_config:
        for script_name in module_config.get('module_installation_scripts'):
            install_execution.logs += f"Run Script: {script_name}\n"
            install_execution.save()
            os.system(f"/bin/sh {path.joinpath(script_name)}")

    new_module.save()
    install_execution.state = 3
    install_execution.logs += f"done ...\n"
    if module_type == 1:
        install_execution.backup_module = new_module
    else:
        install_execution.storage_module = new_module
    install_execution.save()
