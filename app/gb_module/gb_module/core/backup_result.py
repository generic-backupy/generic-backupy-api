class BackupResult:

    def __init__(self,
                 raw_backup=None,
                 backup_temp_location=None,
                 output=None,
                 error=None):
        # if the backup is small enough, to save it in this variable
        # (don't use it for big backups because of the RAM)
        self.raw_backup = raw_backup
        # temporary location of a backup, if it was needed to save it on the device
        self.backup_temp_location = backup_temp_location
        # string output of a backup, which is an information or similar
        self.output = output
        # error
        self.error = error
