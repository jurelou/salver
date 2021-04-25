# -*- coding: utf-8 -*-
import socket
from uuid import uuid4

from salver.common import models
from salver.agent.api import AgentAPI
from salver.agent.services import kafka_producers


class SalverAgent:
    def __init__(self):
        self.name = f'agent-{socket.getfqdn()}-{uuid4().hex[:4]}'
        self.api = AgentAPI(agent_name=self.name)

    def start(self):

        info_res = kafka_producers.make_agent_info_response()
        info_res.produce(models.AgentInfo(name='init agent xxx'), flush=True)

        self.api.start()


agent = SalverAgent()
agent.start()
