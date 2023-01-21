from django.test import TestCase
from django.db import IntegrityError

from api.models import StorageExecution, BackupJob, Backup, StorageModule, User


class TestModelStorageExecution(TestCase):
    def setUp(self):
        db = StorageExecution.objects.all()
        db.delete()

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            StorageExecution.objects.create(backup_job=None)

    def test_create_required_fields_only(self):
        dummy = BackupJob.objects.create(name="name")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object not added to db")
        StorageExecution.objects.create(backup_job=dummy)
        db = StorageExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy, "Error in field 'backup_job'")
        self.assertEqual(db[0].state, 1, "Wrong default value in field 'state'")

    def test_create_more_fields(self):
        dummy = BackupJob.objects.create(name="name")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object not added to db")
        StorageExecution.objects.create(backup_job=dummy, state=2, output="test", logs="test")
        db = StorageExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy, "Error in field 'backup_job'")
        self.assertEqual(db[0].state, 2, "Error in field 'state'")
        self.assertEqual(db[0].output, "test", "Error in field 'output'")
        self.assertEqual(db[0].logs, "test", "Error in field 'logs'")

    def test_create_foreignkey(self):
        dummy_bj = BackupJob.objects.create(name="name")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (backup_job) not added to db")
        dummy_sm = StorageModule.objects.create(name="name")
        dummy_db = StorageModule.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (storage_module) not added to db")
        StorageExecution.objects.create(backup_job=dummy_bj, storage_module=dummy_sm)
        db = StorageExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy_bj, "Error in field 'backup_job'")
        self.assertEqual(db[0].storage_module, dummy_sm, "Error in field 'storage_module'")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")
        dummy_backup = Backup.objects.create(name="name")
        dummy_db = Backup.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (backup) not added to db")
        StorageExecution.objects.create(backup_job=dummy_bj, involved_backup=dummy_backup)
        db = StorageExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy_bj, "Error in field 'backup_job'")
        self.assertEqual(db[0].involved_backup, dummy_backup, "Error in field 'involved_backup'")


    def test_create_wrong_foreignkey(self):
        dummy_bj = BackupJob.objects.create(name="name")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (backup_job) not added to db")
        dummy = User.objects.create()
        dummy_db = User.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (bckup_module) not added to db")
        with self.assertRaises(ValueError, msg="Wrong data type not detected (storage_module)"):
            StorageExecution.objects.create(backup_job=dummy_bj, storage_module=dummy)
        with self.assertRaises(ValueError, msg="Wrong data type not detected (invoked_backup)"):
            StorageExecution.objects.create(backup_job=dummy_bj, involved_backup=dummy)
