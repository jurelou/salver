# -*- coding: utf-8 -*-
from multiprocessing import Manager

from loguru import logger

from salver.common.kafka import ConsumerCallback
from salver.engine.services import kafka_producers

AVAILABLE_AGENTS = Manager().dict()


class OnAgentConnect(ConsumerCallback):
    def __init__(self):
        # print("NEW", a)
        # self.a = a
        self.agents_broadcast_producer = kafka_producers.make_agent_broadcast_ping()

    def on_message(self, agent_info):
        logger.info(f'Got agent connect from {agent_info.name}')
        AVAILABLE_AGENTS[agent_info.name] = agent_info
        logger.debug(f'available agents: {list(AVAILABLE_AGENTS.keys())}')

        # self.agents_broadcast_producer.produce(
        #     models.PingRequest(ping='enginepinginging'),
        #     flush=True,
        # )


def on_agent_disconnect(agent_info):
    logger.info(f'Got agent disconnect from {agent_info}')
    AVAILABLE_AGENTS.pop(agent_info.name, None)

    logger.debug(f'available agents: {list(AVAILABLE_AGENTS.keys())}')
