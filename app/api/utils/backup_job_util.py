from api.models import BackupJob, BackupJobSecret, BackupJobStorageModuleSecret, BackupJobStorageModule, Parameter
from api.serializers import BackupJobSecretGbModuleSerializer, BackupJobStorageModuleSecretGbModuleSerializer, \
    ParameterGbModuleSerializer


class BackupJobUtil:
    @staticmethod
    def parsed_parameter_dict(backup_job: BackupJob):
        backup_parameters = Parameter.objects.filter(backup_job_parameter_parameter__backup_job=backup_job).distinct()
        param_array = [dict(d) for d in ParameterGbModuleSerializer(backup_parameters, many=True).data]
        param_dict = {}
        for param_el in param_array:
            param_dict |= param_el.get('parameter') or {}
        return param_dict

    @staticmethod
    def parsed_secret_array(backup_job: BackupJob):
        backup_secrets = BackupJobSecret.objects.filter(backup_job=backup_job)
        return [dict(d) for d in BackupJobSecretGbModuleSerializer(backup_secrets, many=True).data]

    @staticmethod
    def parsed_secret_dict(backup_job: BackupJob):
        secret_array = BackupJobUtil.parsed_secret_array(backup_job)
        return {sec.get('key'): sec.get('secret') for sec in secret_array if sec.get('key')}

    @staticmethod
    def parsed_storage_secret_array(backup_job_storage_module: BackupJobStorageModule):
        backup_secrets = BackupJobStorageModuleSecret.objects.filter(backup_job_storage_module=backup_job_storage_module)
        return [dict(d) for d in BackupJobStorageModuleSecretGbModuleSerializer(backup_secrets, many=True).data]

    @staticmethod
    def parsed_storage_secret_dict(backup_job_storage_module: BackupJobStorageModule):
        secret_array = BackupJobUtil.parsed_storage_secret_array(backup_job_storage_module)
        return {sec.get('key'): sec.get('secret') for sec in secret_array if sec.get('key')}

    @staticmethod
    def parsed_storage_parameter_dict(backup_job_storage_module: BackupJobStorageModule):
        storage_parameters = Parameter.objects.filter(
            backup_job_storage_model_parameter_parameter__backup_job_storage_module=backup_job_storage_module
        ).distinct()
        param_array = [dict(d) for d in ParameterGbModuleSerializer(storage_parameters, many=True).data]
        param_dict = {}
        for param_el in param_array:
            param_dict |= param_el.get('parameter') or {}
        return param_dict
