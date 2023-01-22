from django.test import TestCase

from api.models import Backup, BackupJob, BackupModule, StorageModule, BackupExecution, StorageExecution, User, \
    BackupJobStorageModule
from django.db import IntegrityError


class TestModelBackup(TestCase):

    def setUp(self):
        db = Backup.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            Backup.objects.create(name=None)

    def test_create_required_fields_only(self):
        Backup.objects.create(name="name")
        db = Backup.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertIsInstance(db[0].id, int, "Object has wrong autogenerated id")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertIsNone(db[0].original_file_name, "Wrong default value in 'original_file_name'")
        self.assertIsNone(db[0].description, "Wrong default value in 'description'")

    def test_create_more_fields(self):
        Backup.objects.create(name="name", original_file_name="file", path="path", description="desc",
                              additional_parameters={})
        db = Backup.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].original_file_name, "file",
                         "Error in field 'original_file_name'")
        self.assertEqual(db[0].path, "path", "Error in field 'path'")
        self.assertEqual(db[0].description, "desc", "Error in field 'description'")
        self.assertEqual(db[0].additional_parameters, {}, "Error in field 'additional_parameters'")

    def create_backup_job_storage_module_dummy(self):
        dummy_sm = StorageModule.objects.create(name="storage")
        dummy_db = StorageModule.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object ('storage_module') not added to db")
        dummy_db = BackupJob.objects.all()
        dummy_bj = dummy_db[0]
        b = BackupJobStorageModule.objects.create(backup_job=dummy_bj, storage_module=dummy_sm)
        db = BackupJobStorageModule.objects.all()
        self.assertEqual(len(db), 1, "Object BJSM not added to db")
        return b


    def test_create_foreignkey(self):
        dummy_bj = BackupJob.objects.create(name="name")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (backup_job), not added to db")
        dummy_bm = BackupModule.objects.create(name="name")
        dummy_db = BackupModule.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (backup_module), not added to db")
        dummy_se = StorageExecution.objects.create(backup_job=dummy_bj)
        dummy_db = StorageExecution.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (storage_execution), not added to db")
        dummy_be = BackupExecution.objects.create(backup_job=dummy_bj)
        dummy_db = BackupExecution.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (backup_execution), not added to db")
        dummy_bjsm = self.create_backup_job_storage_module_dummy()
        Backup.objects.create(name="name", backup_job=dummy_bj, backup_module=dummy_bm,
                              storage_execution=dummy_se, backup_execution=dummy_be,
                              backup_job_storage_module=dummy_bjsm)
        db = Backup.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].name, "name", "Error in field 'name'")
        self.assertEqual(db[0].backup_job, dummy_bj, "Error in field 'backup_job'")
        self.assertEqual(db[0].backup_module, dummy_bm, "Error in field 'backup_module'")
        self.assertEqual(db[0].backup_execution, dummy_be, "Error in field 'backup_execution'")
        self.assertEqual(db[0].backup_job_storage_module, dummy_bjsm, "Error in field 'backup_job_storage_module'")
        self.assertEqual(db[0].storage_execution, dummy_se, "Error in field 'storage_execution'")

    def test_crete_wrong_foreignkey(self):
        dummy = User.objects.create()
        dummy_db = User.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object not created")
        with self.assertRaises(ValueError, msg="Wrong data type detected (backup_job)"):
            Backup.objects.create(name="name", backup_job=dummy)
        with self.assertRaises(ValueError, msg="Wrong data type detected (backup_module)"):
            Backup.objects.create(name="name", backup_module=dummy)
        with self.assertRaises(ValueError, msg="Wrong data type detected (backup_execution)"):
            Backup.objects.create(name="name", backup_execution=dummy)
        with self.assertRaises(ValueError, msg="Wrong data type detected (storage_module)"):
            Backup.objects.create(name="name", backup_job_storage_module=dummy)
        with self.assertRaises(ValueError, msg="Wrong data type detected (storage_execution)"):
            Backup.objects.create(name="name", storage_execution=dummy)



    def test_delete(self):
        Backup.objects.create(name="name")
        db = Backup.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")
