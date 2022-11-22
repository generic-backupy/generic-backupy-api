from django_rq import job
from api.models import Backup
import time

@job
def test(a, b):
    time.sleep(10)
    Backup.objects.create(name=f"TEST FROM ASYNC, {a}")
