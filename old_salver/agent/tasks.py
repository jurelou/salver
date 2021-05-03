# -*- coding: utf-8 -*-
from typing import List

from celery import current_task
from loguru import logger

from salver.agent import exceptions
from salver.config import agent_config
from salver.agent.app import celery_app, all_collectors, logstash_client
from salver.common.exceptions import BucketFullException
from salver.common.models.fact import BaseFact


@celery_app.task(name='ping')
def ping():
    logger.info('ping')
    return 'pong'


@celery_app.task(name='scan', bind=True, max_retries=3)
def scan(self, facts: List[BaseFact]):
    collector_name = current_task.request.delivery_info['routing_key']

    logger.info(f'Scanning {len(facts)} facts with {collector_name}')

    # Check if collector exists
    if collector_name not in all_collectors:
        logger.debug(f'Collector {collector_name} not found')
        raise exceptions.CollectorNotFound(collector_name)

    # Check if collector is active
    if not all_collectors[collector_name]['active']:
        logger.debug(f'Collector {collector_name} is not active')
        raise exceptions.CollectorDisabled(collector_name)

    collector = all_collectors[collector_name]['instance']

    try:
        collect_result, facts = collector.collect(facts)
    except BucketFullException as err:
        logger.warning(f'Retry scan of {collector_name} in {err.remaining_time}s')
        raise self.retry(countdown=err.remaining_time, exc=err)

    logstash_client.send_facts(facts)
    return collect_result.dict()
