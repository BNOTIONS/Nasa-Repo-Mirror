from celery import task
from celery.decorators import periodic_task
import datetime


@task()
def add(x, y):
    return x + y

# @periodic_task(run_every=datetime.timedelta(minutes=5))
# def sync():
#     return 1 + 1
