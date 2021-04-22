# -*- coding: utf-8 -*-
import multiprocessing

from loguru import logger

from salver.common.models import Collector
from salver.controller.app import celery_app

manager = multiprocessing.Manager()
AVAILABLE_AGENTS = manager.dict()

COLLECTORS_NAMES = manager.list()


def get_agents():
    return AVAILABLE_AGENTS


def get_collectors_names():
    return COLLECTORS_NAMES


def refresh_agents():
    global AVAILABLE_AGENTS
    global COLLECTORS_NAMES

    workers = celery_app.control.inspect().active_queues() or {}
    agents = {}
    c_names = []
    for name in workers.keys():
        conf = celery_app.control.inspect([name]).conf()[name]
        if 'collectors' not in conf:
            continue
        collectors = [Collector(**collector) for collector in conf['collectors']]
        c_names.extend([c.config.name for c in collectors])
        agents[name] = collectors

    AVAILABLE_AGENTS = agents
    COLLECTORS_NAMES = c_names
    logger.info(f'Available agents: {AVAILABLE_AGENTS.keys()}')
