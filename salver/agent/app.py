# -*- coding: utf-8 -*-
from kombu import Queue
from loguru import logger
from celery.signals import worker_init
from celery.schedules import crontab

from salver.config import agent_config
from salver.common.celery import create_app
from salver.common.models import Collector
from salver.agent.collectors.factory import CollectorFactory

all_collectors = CollectorFactory().build()
print("ALL COLLECTORS", all_collectors)
queues = [Queue(name) for name, config in all_collectors.items() if config["active"]]

# Create celery app
celery_app = create_app()
celery_app.conf.update(
    {
        "collectors": [
            Collector(
                config=collector["instance"].config,
                active=collector["active"],
                input_facts=[
                    fact.schema()["title"]
                    for fact in collector["instance"].callbacks().keys()
                ],
            ).dict()
            for collector in all_collectors.values()
        ],
        # "collectors": {
        #     c_name: {
        #         "active": c_item["active"],
        #         "config": c_item["instance"].config.dict(),
        #         "input": [
        #             fact.schema()["title"]
        #             for fact in c_item["instance"].callbacks().keys()
        #         ],
        #     }
        #     for c_name, c_item in all_collectors.items()
        # },
        "imports": "salver.agent.tasks",
        "task_queues": queues,
    },
)


celery_app.conf.update(agent_config.celery)


if __name__ == "__main__":
    argv = [
        "-A",
        "salver.agent.app",
        "worker",
        "--hostname=agent_main",
    ]
    celery_app.worker_main(argv)