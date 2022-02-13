import uuid
from typing import List

from celery import current_task

from salver.agent.app import celery_app, logstash_client
from salver.common.facts import BaseFact
from salver.agent.collectors import all_collectors


@celery_app.task(name="scan")
def scan(scan_id: uuid.UUID, facts: List[BaseFact]):
    collector_name = current_task.request.delivery_info["routing_key"]

    collect_result = all_collectors[collector_name]["instance"].collect(scan_id, facts)
    for f in collect_result:
        logstash_client.send_fact(source=collector_name, fact=f)


