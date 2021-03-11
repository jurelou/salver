from celery.schedules import crontab
from celery.signals import worker_init
from kombu import Queue
from loguru import logger

from opulence.agent.collectors.factory import CollectorFactory
from opulence.common.celery import create_app
from opulence.common.database.es.utils import create_client
from opulence.config import agent_config

all_collectors = CollectorFactory().build()
queues = [Queue(collector) for collector in all_collectors.keys()]

# Create celery app
celery_app = create_app()
celery_app.conf.update(
    {
        "collectors": {
            c_name: {
                "active": c_item["active"],
                "config": c_item["instance"].config.dict(),
                "input": [
                    fact.schema()["title"]
                    for fact in c_item["instance"].callbacks().keys()
                ],
            }
            for c_name, c_item in all_collectors.items()
        },
        "imports": "opulence.agent.tasks",
        "task_queues": queues,
    },
)


celery_app.conf.update(agent_config.celery)

# Create ES instance
es_client = create_client(agent_config.elasticsearch)
