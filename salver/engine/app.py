# -*- coding: utf-8 -*-
from celery.signals import worker_init, worker_ready
from loguru import logger
import celery

from salver.engine import settings
from salver.common.celery import configure_celery

celery_app = configure_celery(config=settings.celery)
celery_app.conf.update(
    {"imports": "salver.engine.tasks",}
)

@worker_init.connect
def init(sender=None, conf=None, **kwargs):
    logger.info("init")

@worker_ready.connect
def ready(sender=None, conf=None, **kwargs):
    logger.info("ready")

    from salver.engine.controllers import agent_tasks

    from salver.engine.scans import Scan
    from salver.engine.scans.single_collector import SingleCollectorStrategy

    from salver.common.facts.personnal.email import Email

    email = Email(address="lol@lol.fr")

    scan = Scan(strategy=SingleCollectorStrategy(collector_name="dummy-collector"))
    scan.run(facts=[email])

    a = celery.current_app.control.inspect().active_queues()
    print("!!!", a)

