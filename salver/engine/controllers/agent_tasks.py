from typing import List

from salver.engine import celery_app
from salver.common.facts import BaseFact


@celery_app.task(ignore_result=True, acks_late=True)
def scan_success(result, scan_id):
    print("Scan done", scan_id)


@celery_app.task
def scan_error(task_id, scan_id):
    print("Scan error", scan_id)


def scan(queue: str, scan_id, facts: List[BaseFact]):
    task = celery_app.send_task(
        "scan",
        link=scan_success.signature([scan_id]),
        link_error=scan_error.signature([scan_id]),
        queue=queue,
        args=[scan_id, facts],
    )
    return task
