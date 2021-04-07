# -*- coding: utf-8 -*-
from typing import List

from celery import current_task
from loguru import logger

from salver.agent.app import celery_app
from salver.agent.collectors.factory import CollectorFactory
from salver.agent import exceptions
from salver.agent.elasticsearch import bulk_upsert
from salver.common.models.fact import BaseFact
from salver.common.exceptions import BucketFullException
from celery import group

all_collectors = CollectorFactory().items


@celery_app.task(name="ping")
def ping(toto):
        print("pingaaa", toto)
        from salver.common.models import ScanResult
        from salver.facts import Person

        a = ScanResult(
            duration=2,
            executions_count=32,
            facts=["Perso"]
        )
        return a


@celery_app.task(name="scan", bind=True, max_retries=3)
def scan(self, facts: List[BaseFact]):

    # return group(B.s(i) for i in range(40))()

    collector_name = current_task.request.delivery_info["routing_key"]
    if collector_name not in all_collectors:
        raise exceptions.CollectorNotFound(collector_name)
    if not all_collectors[collector_name]["active"]:
        raise exceptions.CollectorDisabled(collector_name)

    collector = all_collectors[collector_name]["instance"]
    try:
        collector.check_rate_limit()
    except BucketFullException as err:
        logger.warning(f"Retry scan of {collector_name} in {err.remaining_time}s")
        raise self.retry(countdown=err.remaining_time, exc=err)

    collect_result, facts = collector.collect(facts)
    bulk_upsert(facts)
    collect_result.dict()

    return collect_result.dict()
