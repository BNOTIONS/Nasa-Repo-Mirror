from celery import task


@task()
def add_task(x, y):
    return x + y