# -*- coding: utf-8 -*-
from salver.engine.services import kafka_producers
from salver.engine.api import EngineAPI
from salver.common import models
from salver.facts import Person, Email


class   SalverEngine:
    def __init__(self):


        self.api = EngineAPI()

    def start(self):

        p = Person(firstname='1', lastname='1')
        e = Email(address='addr')
        c = models.CollectRequest(collector_name='toto', facts=[p, e])


        agent_info_prod = kafka_producers.make_agent_info()
        agent_info_prod.produce(models.AgentInfoRequest(), flush=True)


        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)

        # self.producers.agents_info.produce(models.AgentInfoRequest(), flush=True)
        # self.producers.agents_broadcast.produce(models.PingRequest(), flush=True)

        self.api.start()


engine = SalverEngine()
engine.start()