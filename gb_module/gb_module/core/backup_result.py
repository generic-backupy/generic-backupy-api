from .base_result import BaseResult


class BackupResult(BaseResult):

    def __init__(self,
                 raw_backup=None,
                 backup_temp_location=None,
                 additional_parameters_dict: dict = None,
                 output=None,
                 error=None,
                 delete_path=None,
                 original_backup_name=None):
        # if the backup is small enough, to save it in this variable
        # (don't use it for big backups because of the RAM)
        self.raw_backup = raw_backup
        # temporary location of a backup, if it was needed to save it on the device
        self.backup_temp_location = backup_temp_location
        # string output of a backup, which is an information or similar
        self.output = output
        # error
        self.error = error
        # delete path, if it is set, this path should be deleted after the execution
        self.delete_path = delete_path
        # real name of the backup, which should be used in the restore process (to have the original backup name like TS345.cfg)
        self.original_backup_name = original_backup_name
        self.additional_parameters_dict = additional_parameters_dict

    @staticmethod
    def with_error(error, output=None, delete_path=None):
        return BackupResult(error=error, output=output, delete_path=delete_path)
