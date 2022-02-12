from typing import List
from celery import current_task
import uuid

from salver.agent import celery_app
from salver.common.facts import BaseFact
from salver.agent.collectors import all_collectors

@celery_app.task(name="scan")
def scan(scan_id: uuid.UUID, facts: List[BaseFact]):
    collector_name = current_task.request.delivery_info["routing_key"]

    collect_result = all_collectors[collector_name]["instance"].collect(scan_id, facts)
    for i in collect_result:
        print(i)