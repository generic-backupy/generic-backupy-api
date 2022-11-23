from gb_module.gb_module.core.backup_module import BackupModule
import time

class GBModule(BackupModule):
    def do_backup(self):
        # simulate long running backup process
        self.log("before timer")
        time.sleep(2)
        self.log("after timer 2 minutes")
        time.sleep(3)
        self.log("after timer 3 minutes")
        time.sleep(2)
        print("hello world :)")
        self.log("done ...")
        return f"new one bro :) {len(self.secrets)}"
