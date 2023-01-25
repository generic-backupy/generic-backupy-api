class ModuleTestUtil:

    @staticmethod
    def create_module(module_class):
        return module_class()

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
    def create_storage_module(module_class, default_path="/default"):
        module = ModuleTestUtil.create_default_module(module_class)
        module.parameters |= {"path": default_path}
        return module

    @staticmethod
    def create_default_module(module_class):
        module = ModuleTestUtil.create_module(module_class)
        module.secrets = {
            "password": "1234"
        }
        module.parameters = {}
        module.system = ModuleTestUtil.create_system_testsystem()
        module.backup_job = ModuleTestUtil.create_backup_job()
        module.log = ModuleTestUtil.create_default_logging_function()
        return module

