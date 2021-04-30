# -*- coding: utf-8 -*-
import sys
import socket
from uuid import uuid4
from signal import SIGTERM, signal
from functools import partial

from loguru import logger

from salver.common import models
from salver.agent.api import AgentAPI
from salver.agent.services import collectors, kafka_producers


class SalverAgent:
    def __init__(self):
        self.name = f'agent-{socket.getfqdn()}-{uuid4().hex[:4]}'
        all_collectors = [
            models.Collector(name=c_name, enabled=c_config['enabled'])
            for c_name, c_config in collectors.ALL_COLLECTORS.items()
        ]
        self.agent_info = models.AgentInfo(name=self.name, collectors=all_collectors)
        self.api = AgentAPI(agent_info=self.agent_info)

    def start(self):
        logger.info(f'Starting agent {self.name}')

        agent_connect = kafka_producers.make_agent_connect()
        agent_disconnect = kafka_producers.make_agent_disconnect()

        agent_connect.produce(self.agent_info, flush=True)

        try:
            self.api.start()
        except KeyboardInterrupt:
            logger.warning('quitting')
            agent_disconnect.produce(self.agent_info, flush=True)
        self.api.stop()


agent = SalverAgent()
agent.start()
