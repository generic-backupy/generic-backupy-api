class ModuleTestUtil:

    @staticmethod
    def create_module(module_class):
        return module_class()

    @staticmethod
    def create_secrets_password():
        return [
            {'id': 1, 'name': "password", 'description': None, 'secret': "1234"}
        ]

    @staticmethod
    def create_parameters_path(path="/backups/default"):
        return [
            {'id': 1, 'name': "default path parameter", 'description': None, 'parameter': {"path": path}}
        ]

    @staticmethod
    def create_system_testsystem():
        return {'id': 1, 'name': "Testsystem", 'description': None, 'host': "localhost", 'additional_information': None}

    @staticmethod
    def create_backup_job(name="TestJob", description=None):
        return {'id': 1, 'name': name, 'description': description}

    @staticmethod
    def create_default_logging_function():
        def storage_log(message):
            message = f"{message}\n"
            print(message)
        return storage_log

    @staticmethod
    def create_storage_module(module_class, path="/default"):
        module = ModuleTestUtil.create_module(module_class)
        module.secrets = ModuleTestUtil.create_secrets_password()
        module.parameters = ModuleTestUtil.create_parameters_path(path=path)
        module.system = ModuleTestUtil.create_system_testsystem()
        module.backup_job = ModuleTestUtil.create_backup_job()
        module.log = ModuleTestUtil.create_default_logging_function()
        return module

    @staticmethod
    def create_default_module(module_class):
        module = ModuleTestUtil.create_module(module_class)
        module.secrets = ModuleTestUtil.create_secrets_password()
        module.parameters = ModuleTestUtil.create_parameters_path()
        module.system = ModuleTestUtil.create_system_testsystem()
        module.backup_job = ModuleTestUtil.create_backup_job()
        module.log = ModuleTestUtil.create_default_logging_function()
        return module

