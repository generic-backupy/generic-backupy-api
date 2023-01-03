from api.models import Category, BackupJob
from api.testing.test_utils.category_test_util import CategoryTestUtil
from api.testing.test_utils.system_test_util import SystemTestUtil


class BackupJobTestUtil:

    @staticmethod
    def create_network_test_backup_jobs():
        switch_1, switch_2, access_point_1, special_switch_1 = SystemTestUtil.create_network_test_categories()

        job_switch_1 = BackupJob.objects.create(name="switch 1", system=switch_1)
        job_switch_2 = BackupJob.objects.create(name="switch 2", system=switch_2)
        job_access_point = BackupJob.objects.create(name="access point 1", system=access_point_1)
        job_special_switch_2 = BackupJob.objects.create(name="special switch 2", system=special_switch_1)

        return job_switch_1, job_switch_2, job_access_point, job_special_switch_2
