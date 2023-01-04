from api.models import BackupModule, StorageModule


class ModuleTestUtil:

    @staticmethod
    def create_invalid_storage_module(name="invalid"):
        return ModuleTestUtil.create_storage_module(name, "invalid/path")

    @staticmethod
    def create_storage_mock_module(name="valid"):
        return ModuleTestUtil.create_storage_module(name, "api/testing/test_files/storage_mock_module")

    @staticmethod
    def create_storage_module(name, path):
        return StorageModule.objects.create(name=name, file_system_path=path)

    @staticmethod
    def create_invalid_backup_module(name="invalid"):
        return ModuleTestUtil.create_backup_module(name, "invalid/path")

    @staticmethod
    def create_backup_mock_module(name="valid"):
        return ModuleTestUtil.create_backup_module(name, "api/testing/test_files/backup_mock_module")

    @staticmethod
    def create_backup_module(name, path):
        return BackupModule.objects.create(name=name, file_system_path=path)

