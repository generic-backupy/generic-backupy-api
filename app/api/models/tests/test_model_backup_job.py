from django.db import IntegrityError
from django.test import TestCase

from api.models.backup_job import *
from api.models import System, BackupModule, User, Secret, Parameter, StorageModule


class TestModelBackupJob(TestCase):

    def setUp(self):
        db = BackupJob.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            BackupJob.objects.create(name=None)

    def test_create_required_fields_only(self):
        BackupJob.objects.create(name="name")
        db = BackupJob.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertIsNone(db[0].description, "Wrong default value in 'description'")
        self.assertIsNone(db[0].additional_information, "Wrong default value in 'additional_information'")
        self.assertIsNone(db[0].system, "Wrong default value in 'system'")
        self.assertIsNone(db[0].backup_module, "Wrong default value in 'backup_module'")

    def test_create_all_fields(self):
        BackupJob.objects.create(name="name", description="desc", additional_information="info")
        db = BackupJob.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].description, "desc", "Error in field 'description'")
        self.assertEqual(db[0].additional_information, "info", "Error in field 'additional_information'")
        self.assertIsNone(db[0].system, "Wrong default value in 'system'")
        self.assertIsNone(db[0].backup_module, "Wrong default value in 'backup_module'")

    def test_create_foreignkey(self):
        system = System.objects.create(name="name")
        dummy_db = System.objects.all()
        self.assertEqual(len(dummy_db), 1, "foreign object 'system' not added to db")
        BackupJob.objects.create(name="name", system=system)
        db = BackupJob.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].system, system, "Error in field 'system")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")
        bm = BackupModule.objects.create(name="name")
        dummy_db = BackupModule.objects.all()
        self.assertEqual(len(dummy_db), 1, "foreign object 'backup_module' not added to db")
        BackupJob.objects.create(name="name", backup_module=bm)
        db = BackupJob.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].backup_module, bm, "Error in field 'backup_module")

    def test_create_wrong_foreignkey(self):
        dummy = User.objects.create()
        dummy_db = User.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object not added to db")
        with self.assertRaises(ValueError, msg="Wrong data type not detected('system')"):
            BackupJob.objects.create(name="name", system=dummy)
        with self.assertRaises(ValueError, msg="Wrong data type not detected('backup_module')"):
            BackupJob.objects.create(name="name", backup_module=dummy)

    def test_delete(self):
        BackupJob.objects.create(name="name")
        db = BackupJob.objects.all()
        self.assertEqual(len(db), 1, "object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")


class TestModelBackupJobSecret(TestCase):

    def setUp(self):
        db = BackupJobSecret.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            BackupJobSecret.objects.create(secret=None, backup_job=None)

    def test_create_required_fields_only(self):
        dummy_secret = Secret.objects.create(name="secret")
        dummy_db = Secret.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('secret') not added to db")
        dummy_bj = BackupJob.objects.create(name="bj")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('backup_job') not added to db")
        BackupJobSecret.objects.create(backup_job=dummy_bj, secret=dummy_secret)
        db = BackupJobSecret.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy_bj, "Error in field 'backup_job'")
        self.assertEqual(db[0].secret, dummy_secret, "Error in field 'secret'")
        self.assertEqual(db[0].key, "", "Wrong default value in field 'key'")

    def test_create_all_fields(self):
        dummy_secret = Secret.objects.create(name="secret")
        dummy_db = Secret.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('secret') not added to db")
        dummy_bj = BackupJob.objects.create(name="bj")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('backup_job') not added to db")
        BackupJobSecret.objects.create(backup_job=dummy_bj, secret=dummy_secret, key="key")
        db = BackupJobSecret.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy_bj, "Error in field 'backup_job'")
        self.assertEqual(db[0].secret, dummy_secret, "Error in field 'secret'")
        self.assertEqual(db[0].key, "key", "Error in field 'key'")


class TestModelBackupJobParameter(TestCase):
    def setUp(self):
        db = BackupJobParameter.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            BackupJobParameter.objects.create(parameter=None, backup_job=None)

    def test_create_required_fields_only(self):
        dummy_parameter = Parameter.objects.create(name="param", parameter={})
        dummy_db = Parameter.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('parameter') not added to db")
        dummy_bj = BackupJob.objects.create(name="bj")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('backup_job') not added to db")
        BackupJobParameter.objects.create(backup_job=dummy_bj, parameter=dummy_parameter)
        db = BackupJobParameter.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy_bj, "Error in field 'backup_job'")
        self.assertEqual(db[0].parameter, dummy_parameter, "Error in field 'parameter'")

    def test_create_all_fields(self):
        dummy_parameter = Parameter.objects.create(name="param", parameter={})
        dummy_db = Parameter.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('parameter') not added to db")
        dummy_bj = BackupJob.objects.create(name="bj")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('backup_job') not added to db")
        BackupJobParameter.objects.create(backup_job=dummy_bj, parameter=dummy_parameter)
        db = BackupJobParameter.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy_bj, "Error in field 'backup_job'")
        self.assertEqual(db[0].parameter, dummy_parameter, "Error in field 'parameter'")


class TestBackupJobStorageModuleSecret(TestCase):
    def setUp(self):
        db = BackupJobStorageModuleSecret.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            BackupJobStorageModuleSecret.objects.create(backup_job_storage_module=None, secret=None)

    def test_create_required_fields_only(self):
        dummy_db = create_backup_job_sm()
        self.assertEqual(len(dummy_db),1,"Dummy object('backup_job_storage_module') not added to db")
        dummy_bjsm = dummy_db[0]
        dummy_secret = Secret.objects.create(name="secret")
        dummy_db = Secret.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object('secret') not added to db")
        BackupJobStorageModuleSecret.objects.create(backup_job_storage_module=dummy_bjsm, secret=dummy_secret)
        db = BackupJobStorageModuleSecret.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].secret, dummy_secret, "Error in field 'secret'")
        self.assertEqual(db[0].backup_job_storage_module, dummy_bjsm, "Error in field 'backup_job_storage_module'")
        self.assertEqual(db[0].key, "", "Wrong default value in field 'key'")

    def test_create_all_fields(self):
        dummy_db = create_backup_job_sm()
        self.assertEqual(len(dummy_db),1,"Dummy object('backup_job_storage_module') not added to db")
        dummy_bjsm = dummy_db[0]
        dummy_secret = Secret.objects.create(name="secret")
        dummy_db = Secret.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object('secret') not added to db")
        BackupJobStorageModuleSecret.objects.create(backup_job_storage_module=dummy_bjsm, secret=dummy_secret, key="key")
        db = BackupJobStorageModuleSecret.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].secret, dummy_secret, "Error in field 'secret'")
        self.assertEqual(db[0].backup_job_storage_module, dummy_bjsm, "Error in field 'backup_job_storage_module'")
        self.assertEqual(db[0].key, "key", "Error in field 'key")


class TestModelBackupJobStorageModule(TestCase):
    def setUp(self):
        db = BackupJobStorageModule.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            BackupJobStorageModule.objects.create(backup_job=None, storage_module=None)

    def test_create_required_fields_only(self):
        dummy_sm = StorageModule.objects.create(name="storage")
        dummy_db = StorageModule.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('storage_module') not added to db")
        dummy_bj = BackupJob.objects.create(name="bj")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('backup_job') not added to db")
        BackupJobStorageModule.objects.create(backup_job=dummy_bj, storage_module=dummy_sm)
        db = BackupJobStorageModule.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy_bj, "Error in field 'backup_job'")
        self.assertEqual(db[0].storage_module, dummy_sm, "Error in field 'secrets'")


def create_backup_job_sm():
    dummy_sm = StorageModule.objects.create(name="storage")
    dummy_bj = BackupJob.objects.create(name="bj")
    BackupJobStorageModule.objects.create(backup_job=dummy_bj, storage_module=dummy_sm)
    return BackupJobStorageModule.objects.all()


class TestBackupJobStorageModuleParameter(TestCase):

    def setUp(self):
        db = BackupJobStorageModuleParameter.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            BackupJobStorageModuleParameter.objects.create(backup_job_storage_module=None, parameter=None)

    def test_create_required_fields_only(self):
        dummy_parameter = Parameter.objects.create(name="param", parameter={})
        dummy_db = Parameter.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('parameter') not added to db")
        dummy_db = create_backup_job_sm()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('backup_job_storage_module') not added to db")
        dummy_bjsm = dummy_db[0]
        BackupJobStorageModuleParameter.objects.create(backup_job_storage_module=dummy_bjsm, parameter=dummy_parameter)
        db = BackupJobStorageModuleParameter.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job_storage_module, dummy_bjsm, "Error in field 'backup_job_storage_module'")
        self.assertEqual(db[0].parameter, dummy_parameter, "Error in field 'parameter'")
