from django.test import TestCase
from django.db import IntegrityError

from api.models import RestoreExecution, Backup, User


class TestModelRestoreExecution(TestCase):
    def setUp(self):
        db = RestoreExecution.objects.all()
        db.delete()

    def create_dummy(self):
        dummy = Backup.objects.create(name="name")
        dummy_db = Backup.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object not added to db")
        return dummy
    def test_create_defaults(self):
        RestoreExecution.objects.create()
        db = RestoreExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].state, 0, "Wrong default value in filed 'state'")

    def test_create_all_fields(self):
        RestoreExecution.objects.create(output="out", logs="log", errors="error", state=1)
        db = RestoreExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].state, 1, "Error in filed 'state'")
        self.assertEqual(db[0].output, "out", "Error in filed 'output'")
        self.assertEqual(db[0].logs, "log", "Error in filed 'logs'")
        self.assertEqual(db[0].errors, "error", "Error in filed 'error'")



    def test_create_foreignkey(self):
        dummy = self.create_dummy()
        RestoreExecution.objects.create(backup_instance=dummy)
        db = RestoreExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        self.assertEqual(db[0].backup_instance, dummy, "Error in field 'backup_instance")


    def test_create_wrong_foreignkey(self):
        dummy = User.objects.create()
        dummy_db = User.objects.all()
        self.assertEqual(len(dummy_db), 1, "Dummy object not added to db")
        with self.assertRaises(ValueError, msg="Wrong type not detected"):
            RestoreExecution.objects.create(backup_instance=dummy)


    def test_delete(self):
        RestoreExecution.objects.create()
        db = RestoreExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        db.delete()
        self.assertEqual(len(db), 0, "Error while deleting")

    def test_str(self):
        dummy = self.create_dummy()
        re = RestoreExecution.objects.create(backup_instance=dummy)
        db = RestoreExecution.objects.all()
        self.assertEqual(len(db), 1, "Object not added to db")
        s = str(re)
        proper_str = f"{re.id} - waiting - name"
        self.assertEqual(s, proper_str, "Error while creating string")
        re = RestoreExecution.objects.create()
        db = RestoreExecution.objects.all()
        self.assertEqual(len(db), 2, "Object not added to db")
        s = str(re)
        proper_str = f"{re.id} - waiting"
        self.assertEqual(s, proper_str, "Error while creating string")
