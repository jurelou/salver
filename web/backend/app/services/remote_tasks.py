
from app.config import settings

from celery import Celery

controller_app = Celery()
controller_app.conf.update(settings.celery)


def async_call(task_name, **kwargs):
    return controller_app.send_task(task_name, **kwargs)

def sync_call(task_name, timeout=10, **kwargs):
    task = async_call(task_name, **kwargs)
    return task.get(timeout=timeout)

