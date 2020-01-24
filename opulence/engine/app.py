from celery.signals import worker_ready

from . import collector_tasks, fact_tasks, scan_tasks  # noqa: W0611
from .scans import tasks as scan_task


# Load things on startup
@worker_ready.connect
def startup(sender=None, conf=None, **kwargs):
    fact_tasks.flush()
    fact_tasks.load()

    scan_task.flush()

    collector_tasks.flush()
    collector_tasks.load()
