from django.test import TestCase
from api.serializers import BackupJobStorageModulePostSerializer
from api.models import Parameter, Secret, StorageModule
from api.models.backup_job import BackupJob, BackupJobStorageModuleSecret, BackupJobStorageModule, \
    BackupJobStorageModuleParameter


class TestSerializerBackupJobStorageModule(TestCase):

    def setUp(self) -> None:
        bj = BackupJob.objects.create(name="backup_job")
        Parameter.objects.create(name="param", parameter={})
        Secret.objects.create(name="sec")
        sm = StorageModule.objects.create(name="sm")
        BackupJobStorageModule.objects.create(backup_job=bj, storage_module=sm)

    def primal_test(self):
        backup_db = BackupJob.objects.all()
        self.assertEqual(len(backup_db), 1, "object BackupModule not added to db")
        param_db = Parameter.objects.all()
        self.assertEqual(len(param_db), 1, "object Parameter not added to db")
        secret_db = Secret.objects.all()
        self.assertEqual(len(secret_db), 1, "object Secret not added to db")
        storage_db = StorageModule.objects.all()
        self.assertEqual(len(storage_db), 1, "object StorageModule not added to db")

    def common_assertions(self, b, test):
        db = BackupJobStorageModule.objects.all()
        self.assertEqual(len(db), 2, "object(s) not added to db")
        self.assertEqual(b.storage_module, test.storage_module, "Object are not identical('storage_module')")
        self.assertEqual(b.backup_job, test.backup_job, "Object are not identical('backup_job')")

    def test_create_without_additional_parameters(self):
        self.primal_test()
        backup_db = BackupJob.objects.all()
        storage_db = StorageModule.objects.all()
        test = BackupJobStorageModule.objects.all()[0]
        b = BackupJobStorageModulePostSerializer().create({'backup_job': backup_db[0],
                                                           'storage_module': storage_db[0]})

        self.common_assertions(b, test)

    def test_create_with_secret(self):
        self.primal_test()
        backup_db = BackupJob.objects.all()
        storage_db = StorageModule.objects.all()
        secret_db = list(Secret.objects.all())
        test = BackupJobStorageModule.objects.all()[0]
        b = BackupJobStorageModulePostSerializer().create({'backup_job': backup_db[0],
                                                           'storage_module': storage_db[0],
                                                           'secret': secret_db})
        BackupJobStorageModuleSecret.objects.create(backup_job_storage_module=test, secret=secret_db[0])
        self.common_assertions(b, test)
        self.assertEqual(b.secrets.all()[0], test.secrets.all()[0],
                         "Object are not identical('secrets')")

    def test_create_with_parameter(self):
        self.primal_test()
        backup_db = BackupJob.objects.all()
        storage_db = StorageModule.objects.all()
        param_db = list(Parameter.objects.all())
        test = BackupJobStorageModule.objects.all()[0]
        b = BackupJobStorageModulePostSerializer().create({'backup_job': backup_db[0],
                                                           'storage_module': storage_db[0],
                                                           'parameter': param_db})
        BackupJobStorageModuleParameter.objects.create(backup_job_storage_module=test, parameter=param_db[0])

        self.common_assertions(b, test)
        self.assertEqual(b.parameters.all()[0], test.parameters.all()[0],
                         "Object are not identical('parameters')")

    def test_create_with_all(self):
        self.primal_test()
        backup_db = BackupJob.objects.all()
        storage_db = StorageModule.objects.all()
        secret_db = list(Secret.objects.all())
        param_db = list(Parameter.objects.all())
        test = BackupJobStorageModule.objects.all()[0]
        b = BackupJobStorageModulePostSerializer().create({'backup_job': backup_db[0],
                                                           'storage_module': storage_db[0],
                                                           'parameter': param_db,
                                                           'secret': secret_db})
        BackupJobStorageModuleParameter.objects.create(backup_job_storage_module=test, parameter=param_db[0])
        BackupJobStorageModuleSecret.objects.create(backup_job_storage_module=test, secret=secret_db[0])
        self.common_assertions(b, test)
        self.assertEqual(b.parameters.all()[0], test.parameters.all()[0],
                         "Object are not identical('parameters')")
        self.assertEqual(b.secrets.all()[0], test.secrets.all()[0],
                         "Object are not identical('secrets')")

    def test_create_with_multiple(self):
        self.primal_test()
        Secret.objects.create(name="secret2")
        backup_db = BackupJob.objects.all()
        storage_db = StorageModule.objects.all()
        secret_db = list(Secret.objects.all())
        self.assertEqual(len(secret_db), 2, "Second object 'secret' not added to db")
        secret_db = list(secret_db)
        test = BackupJobStorageModule.objects.all()[0]
        b = BackupJobStorageModulePostSerializer().create({'backup_job': backup_db[0],
                                                           'storage_module': storage_db[0],
                                                           'secret': secret_db})

        BackupJobStorageModuleSecret.objects.create(backup_job_storage_module=test, secret=secret_db[0])
        BackupJobStorageModuleSecret.objects.create(backup_job_storage_module=test, secret=secret_db[1])
        self.common_assertions(b, test)
        b_secrets = list(b.secrets.all())
        test_secrets = list(test.secrets.all())
        self.assertEqual(b_secrets, test_secrets,
                         "Object are not identical('secrets')")
