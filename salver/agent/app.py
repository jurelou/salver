# -*- coding: utf-8 -*-
from salver.agent.services import kafka_producers

from salver.agent.api import AgentAPI
from salver.common import models


class   SalverAgent:
    def __init__(self):
        self.api = AgentAPI()

    def start(self):

        info_res = kafka_producers.make_info_response()
        info_res.produce(models.AgentInfo(name="fromhere"), flush=True)

        self.api.start()


agent = SalverAgent()
agent.start()