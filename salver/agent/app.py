# -*- coding: utf-8 -*-
from kombu import Queue
from celery.signals import worker_process_init, worker_process_shutdown, worker_shutdown
from celery.schedules import crontab
from loguru import logger
from salver.config import agent_config
from salver.common.celery import create_app
from salver.common.models import Collector
from salver.agent.services.logstash import LogstashInput
from salver.agent.collectors.factory import CollectorFactory

all_collectors = CollectorFactory().build()


queues = [Queue(name) for name, config in all_collectors.items() if config["active"]]
logstash_client = LogstashInput(
    host=agent_config.logstash.host,
    port=agent_config.logstash.port,
)

collectors_conf = []
for collector_name, collector_config in all_collectors.items():
    config = None
    input_facts = None
    active = collector_config["active"]
    if active:
        config = collector_config["instance"].config
        input_facts = [
            fact.schema()["title"]
            for fact in collector_config["instance"].callbacks().keys()
        ]

    collectors_conf.append(
        Collector(
            config=config,
            name=collector_name,
            active=active,
            input_facts=input_facts,
        ),
    )

# Create celery app
celery_app = create_app()
celery_app.conf.update(
    {
        "collectors": [c.dict() for c in collectors_conf],
        "imports": "salver.agent.tasks",
        "task_queues": queues,
    },
)


celery_app.conf.update(agent_config.celery)

# Hack for coverage.
# See: https://github.com/nedbat/coveragepy/issues/689
IS_TESTING = agent_config.ENV_FOR_DYNACONF == "testing"
if IS_TESTING:
    from coverage import Coverage # pragma: nocover
    COVERAGE = None

@worker_process_init.connect
def on_init(sender=None, conf=None, **kwargs):
    try:
        if IS_TESTING:
            global COVERAGE
            COVERAGE = Coverage(data_suffix=True)
            COVERAGE.start()
    except Exception as err:
        logger.critical(f"Error in signal `worker_process_init`: {err}")

@worker_shutdown.connect
def on_shutdown(**kwargs):
    try:
        logstash_client.close()
    except Exception as err:
        logger.critical(f"Error in signal `worker_shutdown`: {err}")


@worker_process_shutdown.connect
def on_process_shutdown(**kwargs):
    try:
        if IS_TESTING and COVERAGE:
            COVERAGE.stop()
            COVERAGE.save()
    except Exception as err:
        logger.critical(f"Error in signal `worker_process_shutdown`: {err}")

if __name__ == "__main__":
    argv = [
        "-A",
        "salver.agent.app",
        "worker",
        "--hostname=agent_main",
    ]
    celery_app.worker_main(argv)
