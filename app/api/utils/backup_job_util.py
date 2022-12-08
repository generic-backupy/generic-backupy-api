from api.models import BackupJob, BackupJobSecret
from api.serializers import BackupJobSecretGbModuleSerializer


class BackupJobUtil:
    @staticmethod
    def parsed_secret_array(backup_job: BackupJob):
        backup_secrets = BackupJobSecret.objects.filter(backup_job=backup_job)
        return [dict(d) for d in BackupJobSecretGbModuleSerializer(backup_secrets, many=True).data]
