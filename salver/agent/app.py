# -*- coding: utf-8 -*-
from kombu import Queue
from loguru import logger
from celery.signals import celeryd_init

from salver.agent.config import settings
from salver.common.celery import configure_celery
from salver.agent.collectors import all_collectors
from salver.agent.logstash import LogstashClient

queues = [Queue(collector) for collector in all_collectors.keys()]

celery_app = configure_celery(config=settings.celery)
celery_app.conf.update({"imports": "salver.agent.tasks", "task_queues": queues})

logstash_client = LogstashClient()

@celeryd_init.connect
def startup(sender=None, conf=None, **kwargs):
    logger.info("init")


