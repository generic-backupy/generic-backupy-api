from gb_module.gb_module.core.backup_module import BackupModule


class GBModule(BackupModule):
    def do_backup(self):
        print("hello world :)")
        return "yo"
