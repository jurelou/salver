# -*- coding: utf-8 -*-
from celery.schedules import crontab
from celery.signals import worker_init
from kombu import Queue
from loguru import logger

from salver.agent.collectors.factory import CollectorFactory
from salver.common.celery import create_app
from salver.config import agent_config

all_collectors = CollectorFactory().build()
print("ALL COLLECTORS", all_collectors)
queues = [Queue(name) for name, config in all_collectors.items() if config["active"]]

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
