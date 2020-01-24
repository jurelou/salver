import celery
from celery.utils.log import get_task_logger

from .exceptions import TaskTimeoutError

logger = get_task_logger(__name__)


def sync_call(app, task_path, timeout=5, **kwargs):
    try:
        task = app.send_task(task_path, **kwargs)
        return task.get(timeout=timeout)
    except celery.exceptions.TimeoutError:
        raise TaskTimeoutError("{}".format(task_path))


def async_call(app, task_path, **kwargs):
    try:
        return app.send_task(task_path, **kwargs)
    except celery.exceptions.TimeoutError:
        raise TaskTimeoutError("{}".format(task_path))
