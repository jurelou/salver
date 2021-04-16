# -*- coding: utf-8 -*-
import multiprocessing

from loguru import logger

from salver.common.models import Collector
from salver.controller.app import celery_app

manager = multiprocessing.Manager()
available_agents = manager.dict()

collectors_names = manager.list()


def get_agents():
    return available_agents


def get_collectors_names():
    return collectors_names


def refresh_agents():
    global available_agents
    global collectors_names

    workers = celery_app.control.inspect().active_queues() or {}
    agents = {}
    c_names = []
    for name in workers.keys():
        conf = celery_app.control.inspect([name]).conf()[name]
        if "collectors" not in conf:
            continue
        collectors = [Collector(**collector) for collector in conf["collectors"]]
        c_names.extend([c.config.name for c in collectors])
        agents[name] = collectors

    available_agents = agents
    collectors_names = c_names
    logger.info(f"Available agents: {available_agents.keys()}")
