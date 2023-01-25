from gb_module.core.backup_result import BackupResult

class BackupResultTestUtil:

    """
    Factory method to create a BackupResult with a raw_backup as string
    """
    @staticmethod
    def create_result_raw_backup(raw_backup="{'v': 1, 'type': 'fake_backup'}", output="Any output", error=None):
        return BackupResult(raw_backup=raw_backup, output=output, error=None)

    """
    Factory method to create a BackupResult with a path to a backup temporal location
    """
    @staticmethod
    def create_result_backup_temp_location(backup_temp_location, output="Any output", error=None):
        return BackupResult(backup_temp_location=backup_temp_location, output=output, error=None)
