from api.models import BackupJob, BackupJobSecret, BackupJobStorageModuleSecret, BackupJobStorageModule
from api.serializers import BackupJobSecretGbModuleSerializer, BackupJobStorageModuleSecretGbModuleSerializer


class BackupJobUtil:
    @staticmethod
    def parsed_secret_array(backup_job: BackupJob):
        backup_secrets = BackupJobSecret.objects.filter(backup_job=backup_job)
        return [dict(d) for d in BackupJobSecretGbModuleSerializer(backup_secrets, many=True).data]

    @staticmethod
    def parsed_storage_secret_array(backup_job_storage_module: BackupJobStorageModule):
        backup_secrets = BackupJobStorageModuleSecret.objects.filter(backup_job_storage_module=backup_job_storage_module)
        return [dict(d) for d in BackupJobStorageModuleSecretGbModuleSerializer(backup_secrets, many=True).data]
