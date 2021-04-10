# -*- coding: utf-8 -*-
import multiprocessing
from typing import List

from loguru import logger

from salver.config import controller_config
from salver.controller.app import celery_app
from salver.common.models import Collector
manager = multiprocessing.Manager()
available_agents = manager.dict()

get_agents = lambda: available_agents


def refresh_agents():
    global available_agents

    def _get_agents():
        workers = celery_app.control.inspect().active_queues() or {}
        for name in workers.keys():
            conf = celery_app.control.inspect([name]).conf()[name]

            yield name, [Collector(**collector) for collector in conf["collectors"]]

    available_agents = {agent: config for agent, config in _get_agents()}
    logger.info(f"Available agents: {available_agents.keys()}")
