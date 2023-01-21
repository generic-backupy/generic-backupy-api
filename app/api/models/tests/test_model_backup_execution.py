from django.test import TestCase
from django.db import IntegrityError

from api.models import BackupExecution, BackupJob, BackupModule, User


class TestModelBackupExecution(TestCase):
    def setUp(self):
        db = BackupExecution.objects.all()
        db.delete()

    def create_dummy(self):
        dummy = BackupJob.objects.create(name="name")
        dummy_db = BackupJob.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object not added to db")
        return dummy

    def test_create_empty_required_fields(self):
        with self.assertRaises(IntegrityError, msg="Non-Null constrain violated"):
            BackupExecution.objects.create(backup_job=None)

    def test_create_required_fields_only(self):
        dummy = self.create_dummy()
        BackupExecution.objects.create(backup_job=dummy)
        db = BackupExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy, "Error in field 'backup_job'")
        self.assertEqual(db[0].state, 1, "Wrong default value in field 'state'")

    def test_create_more_fields(self):
        dummy = self.create_dummy()
        BackupExecution.objects.create(backup_job=dummy, state = 2, output="test", logs="test")
        db = BackupExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy, "Error in field 'backup_job'")
        self.assertEqual(db[0].state, 2, "Error in field 'state'")
        self.assertEqual(db[0].output, "test", "Error in field 'output'")
        self.assertEqual(db[0].logs, "test", "Error in field 'logs'")

    def test_create_foreignkey(self):
        dummy_bj = self.create_dummy()
        dummy_bm = BackupModule.objects.create(name="name")
        dummy_db = BackupModule.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (bckup_module) not added to db")
        BackupExecution.objects.create(backup_job=dummy_bj, backup_module=dummy_bm)
        db = BackupExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_job, dummy_bj, "Error in field 'backup_job'")
        self.assertEqual(db[0].backup_module, dummy_bm, "Error in field 'backup_module'")

    def test_create_wrong_foreignkey(self):
        dummy_bj = self.create_dummy()
        dummy = User.objects.create()
        dummy_db = User.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object (backup_module) not added to db")
        with self.assertRaises(ValueError, msg="Wrong data type not detected"):
            BackupExecution.objects.create(backup_job=dummy_bj, backup_module=dummy)

    def test_delete(self):
        dummy = self.create_dummy()
        BackupExecution.objects.create(backup_job=dummy)
        db = BackupExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")


