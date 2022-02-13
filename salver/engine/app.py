# -*- coding: utf-8 -*-
import celery
from loguru import logger
import time
from celery.signals import worker_init, worker_ready

from salver.engine.config import settings
from salver.common.celery import configure_celery

celery_app = configure_celery(config=settings.celery)
celery_app.conf.update(
    {
        "imports": "salver.engine.tasks",
        "beat_schedule": {
            'ping-agents-every-x-seconds': {
                'task': 'ping_agents',
                'schedule': settings.ping_agents_delay
            }

        }
    }
)


@worker_init.connect
def ready(sender=None, conf=None, **kwargs):
    from salver.engine.tasks import ping_agents

    ping_agents.apply()
    logger.info("engine ready")


