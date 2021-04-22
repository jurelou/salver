# -*- coding: utf-8 -*-
from typing import List

from celery import current_task
from loguru import logger

from salver.agent import exceptions
from salver.agent.app import celery_app
from salver.config import agent_config
from salver.common.exceptions import BucketFullException
from salver.common.models.fact import BaseFact
from salver.agent.services.logstash import LogstashInput
from salver.agent.collectors.factory import CollectorFactory

all_collectors = CollectorFactory().items
logstash_client = LogstashInput(host=agent_config.logstash.host, port=agent_config.logstash.port)


@celery_app.task(name='ping')
def ping():
    return 'pong'


@celery_app.task(name='scan', bind=True, max_retries=3)
def scan(self, facts: List[BaseFact]):
    collector_name = current_task.request.delivery_info['routing_key']

    print('@@@@@@', facts)

    if collector_name not in all_collectors:
        raise exceptions.CollectorNotFound(collector_name)
    if not all_collectors[collector_name]['active']:
        raise exceptions.CollectorDisabled(collector_name)

    collector = all_collectors[collector_name]['instance']
    try:
        collector.check_rate_limit()
    except BucketFullException as err:
        logger.warning(f'Retry scan of {collector_name} in {err.remaining_time}s')
        raise self.retry(countdown=err.remaining_time, exc=err)

    collect_result, facts = collector.collect(facts)

    logstash_client.send_facts(facts)

    collect_result.dict()
    print('RETURN', collect_result.dict())
    return collect_result.dict()
