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
    }
)


@worker_init.connect
def init(sender=None, conf=None, **kwargs):
    logger.info("init")


@worker_ready.connect
def ready(sender=None, conf=None, **kwargs):
    logger.info("ready")

    from salver.engine.scans import Scan
    from salver.engine.controllers import agent_tasks
    from salver.common.facts.personnal.email import Email
    from salver.engine.scans.single_collector import SingleCollectorStrategy

    scan = Scan(strategy=SingleCollectorStrategy(collector_name="dummy-docker-collector"))

    scan.run(facts=[Email(address="aa")])
    scan.run(facts=[Email(address="bb")])
    scan.run(facts=[Email(address="cc")])

    a = celery.current_app.control.inspect().active_queues()
    print("!!!", a)
