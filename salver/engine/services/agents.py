# -*- coding: utf-8 -*-
from multiprocessing import Manager

from loguru import logger

from salver.common.kafka import ConsumerCallback
from salver.engine.services import kafka_producers

AVAILABLE_AGENTS = Manager().dict()


def get_collectors_mapping():
    mapping = {}
    for agent in AVAILABLE_AGENTS.values():
        for collector in agent.collectors:
            for allowed_input in collector.allowed_input:
                if allowed_input in mapping:
                    mapping[allowed_input].append(collector.name)
                else:
                    mapping[allowed_input] = [collector.name]
    return mapping


def on_agent_connect(agent_info):
    logger.info(f"Got agent connect from {agent_info.name}")
    AVAILABLE_AGENTS[agent_info.name] = agent_info
    logger.debug(f"available agents: {list(AVAILABLE_AGENTS.keys())}")


def on_agent_disconnect(agent_info):
    logger.info(f"Got agent disconnect from {agent_info}")
    AVAILABLE_AGENTS.pop(agent_info.name, None)

    logger.debug(f"available agents: {list(AVAILABLE_AGENTS.keys())}")


def agent_collect():
    pass
