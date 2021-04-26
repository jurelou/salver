# -*- coding: utf-8 -*-
import socket
from uuid import uuid4

from salver.common import models
from salver.agent.api import AgentAPI
from salver.agent.services import kafka_producers
from loguru import logger

class SalverAgent:
    def __init__(self):
        self.name = f'agent-{socket.getfqdn()}-{uuid4().hex[:4]}'
        self.api = AgentAPI(agent_name=self.name)

    def start(self):
        logger.info(f'Starting agent {self.name}')

        info_res = kafka_producers.make_agent_info_response()
        info_res.produce(models.AgentInfo(name=self.name), flush=True)

        self.api.start()


agent = SalverAgent()
agent.start()
