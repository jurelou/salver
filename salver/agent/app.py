# -*- coding: utf-8 -*-
from kombu import Queue
from loguru import logger
from celery.signals import celeryd_init
from celery.schedules import crontab

from salver.agent.config import settings
from salver.common.celery import configure_celery
from salver.agent.collectors import all_collectors
from salver.agent.logstash import LogstashClient

queues = [Queue(collector) for collector in all_collectors.keys()]

celery_app = configure_celery(config=settings.celery)

celery_app.conf.update(
    {
        "imports": "salver.agent.tasks",
        "task_queues": queues,
        "collectors": {
            c_name: {
                "enabled": collector["enabled"],
                "allowed_input": collector["allowed_input"],
                "config": collector["instance"].config.dict()
            }
            for c_name, collector in all_collectors.items()
        }
    }
)

logstash_client = LogstashClient()


@celeryd_init.connect
def startup(sender=None, conf=None, **kwargs):
    logger.info("init")


