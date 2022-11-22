from gb_module.gb_module.core.backup_module import BackupModule
import time

class GBModule(BackupModule):
    def do_backup(self):
        # simulate long running backup process
        time.sleep(5)
        print("hello world :)")
        return "new one bro :)"
