from django.test import TestCase
from api.serializers import BackupJobPostSerializer
from api.models import System, BackupModule, Parameter, Secret, StorageModule
from api.models.backup_job import BackupJob, BackupJobSecret, BackupJobParameter, BackupJobStorageModule


class TestSerializerBackupJob(TestCase):

    def setUp(self) -> None:
        sys = System.objects.create(name="sys")
        bm = BackupModule.objects.create(name="backup_mod")
        Parameter.objects.create(name="param", parameter={})
        Secret.objects.create(name="sec")
        StorageModule.objects.create(name="sm")
        BackupJob.objects.create(name="name", description="desc", additional_information="info",
                                        system=sys, backup_module=bm)

    def primal_test(self):
        system_db = System.objects.all()
        self.assertEqual(len(system_db), 1, "object System not added to db")
        backup_db = BackupModule.objects.all()
        self.assertEqual(len(backup_db), 1, "object BackupModule not added to db")
        param_db = Parameter.objects.all()
        self.assertEqual(len(param_db), 1, "object Parameter not added to db")
        secret_db = Secret.objects.all()
        self.assertEqual(len(secret_db), 1, "object Secret not added to db")
        storage_db = StorageModule.objects.all()
        self.assertEqual(len(storage_db), 1, "object StorageModule not added to db")

    def common_assertions(self, b, test):
        db = BackupJob.objects.all()
        self.assertEqual(len(db), 2, "object(s) not added to db")
        self.assertEqual(b.name, test.name, "Object are not identical('name')")
        self.assertEqual(b.description, test.description, "Object are not identical('description')")
        self.assertEqual(b.additional_information, test.additional_information,
                         "Object are not identical('additional_information')")
        self.assertEqual(b.system, test.system, "Object are not identical('system')")
        self.assertEqual(b.backup_module, test.backup_module, "Object are not identical('backup_module')")


    def test_create_without_additional_parameters(self):
        self.primal_test()
        system_db = System.objects.all()
        backup_db = BackupModule.objects.all()
        test = BackupJob.objects.all()[0]
        b = BackupJobPostSerializer().create({'name': 'name', 'description': 'desc',
                                              'additional_information': 'info',
                                              'system': system_db[0],
                                              'backup_module': backup_db[0]})
        self.common_assertions(b, test)

    def test_create_with_secret(self):
        self.primal_test()
        system_db = System.objects.all()
        backup_db = BackupModule.objects.all()
        secret_db = list(Secret.objects.all())
        test = BackupJob.objects.all()[0]
        b = BackupJobPostSerializer().create({'name': 'name', 'description': 'desc',
                                              'additional_information': 'info',
                                              'system': system_db[0],
                                              'backup_module': backup_db[0],
                                              'secrets': secret_db})

        BackupJobSecret.objects.create(backup_job=test, secret=secret_db[0])
        self.common_assertions(b, test)
        self.assertEqual(b.backup_module_secrets.all()[0], test.backup_module_secrets.all()[0],
                         "Object are not identical('secrets')")

    def test_create_with_parameter(self):
        self.primal_test()
        system_db = System.objects.all()
        backup_db = BackupModule.objects.all()
        param_db = list(Parameter.objects.all())
        test = BackupJob.objects.all()[0]
        b = BackupJobPostSerializer().create({'name': 'name', 'description': 'desc',
                                              'additional_information': 'info',
                                              'system': system_db[0],
                                              'backup_module': backup_db[0],
                                              'parameters': param_db})

        BackupJobParameter.objects.create(backup_job=test, parameter=param_db[0])
        self.common_assertions(b, test)
        self.assertEqual(b.backup_module_parameters.all()[0], test.backup_module_parameters.all()[0],
                         "Object are not identical('parameter')")

    def test_create_with_storage(self):
        self.primal_test()
        system_db = System.objects.all()
        backup_db = BackupModule.objects.all()
        storage_db = list(StorageModule.objects.all())
        test = BackupJob.objects.all()[0]
        b = BackupJobPostSerializer().create({'name': 'name', 'description': 'desc',
                                              'additional_information': 'info',
                                              'system': system_db[0],
                                              'backup_module': backup_db[0],
                                              'storage_module': storage_db})

        BackupJobStorageModule.objects.create(backup_job=test, storage_module=storage_db[0])
        self.common_assertions(b, test)
        self.assertEqual(b.storage_modules.all()[0], test.storage_modules.all()[0],
                         "Object are not identical('storage_module')")
    def test_create_with_all(self):
        self.primal_test()
        system_db = System.objects.all()
        backup_db = BackupModule.objects.all()
        secret_db = list(Secret.objects.all())
        param_db = list(Parameter.objects.all())
        storage_db = list(StorageModule.objects.all())
        test = BackupJob.objects.all()[0]
        b = BackupJobPostSerializer().create({'name': 'name', 'description': 'desc',
                                              'additional_information': 'info',
                                              'system': system_db[0],
                                              'backup_module': backup_db[0],
                                              'parameters': param_db,
                                              'secrets': secret_db,
                                              'storage_module': storage_db})

        BackupJobStorageModule.objects.create(backup_job=test, storage_module=storage_db[0])
        BackupJobParameter.objects.create(backup_job=test, parameter=param_db[0])
        BackupJobSecret.objects.create(backup_job=test, secret=secret_db[0])
        self.common_assertions(b, test)
        self.assertEqual(b.backup_module_secrets.all()[0], test.backup_module_secrets.all()[0],
                         "Object are not identical('secrets')")
        self.assertEqual(b.backup_module_parameters.all()[0], test.backup_module_parameters.all()[0],
                         "Object are not identical('parameter')")
        self.assertEqual(b.storage_modules.all()[0], test.storage_modules.all()[0],
                         "Object are not identical('storage_module')")

    def test_create_with_multiple(self):
        self.primal_test()
        Secret.objects.create(name= "secret2")
        system_db = System.objects.all()
        backup_db = BackupModule.objects.all()
        secret_db = Secret.objects.all()
        self.assertEqual(len(secret_db),2, "Second object 'secret' not added to db")
        secret_db = list(secret_db)
        test = BackupJob.objects.all()[0]
        b = BackupJobPostSerializer().create({'name': 'name', 'description': 'desc',
                                              'additional_information': 'info',
                                              'system': system_db[0],
                                              'backup_module': backup_db[0],
                                              'secrets': secret_db})

        BackupJobSecret.objects.create(backup_job=test, secret=secret_db[0])
        BackupJobSecret.objects.create(backup_job=test, secret=secret_db[1])
        self.common_assertions(b, test)
        b_secrets = list(b.backup_module_secrets.all())
        test_secrets = list(test.backup_module_secrets.all())
        self.assertEqual(b_secrets, test_secrets,
                         "Object are not identical('secrets')")