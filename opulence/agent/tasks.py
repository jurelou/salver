# -*- coding: utf-8 -*-
from typing import List

from celery import current_task
from loguru import logger

from opulence.agent.app import celery_app
from opulence.agent.collectors.factory import CollectorFactory
from opulence.agent import exceptions
from opulence.agent.elasticsearch import bulk_upsert
from opulence.common.models.fact import BaseFact

all_collectors = CollectorFactory().items


@celery_app.task(name="scan")
def scan(facts: List[BaseFact]):
    collector_name = current_task.request.delivery_info["routing_key"]

    if collector_name not in all_collectors:
        raise exceptions.CollectorNotFound(collector_name)
    if not all_collectors[collector_name]["active"]:
        raise exceptions.CollectorDisabled(collector_name)

    collect_result = all_collectors[collector_name]["instance"].collect(facts)

    bulk_upsert(collect_result.facts)
    result = collect_result.dict(exclude={"facts"})
    result["facts"] = [fact.hash__ for fact in collect_result.facts]
    return result
