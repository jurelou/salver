# -*- coding: utf-8 -*-
from salver.facts import Email, Person
from salver.common import models
from salver.engine.api import EngineAPI
from salver.engine.services import kafka_producers


class SalverEngine:
    def __init__(self):

        self.api = EngineAPI(on_start=self.on_engine_start)

    def on_engine_start(self):
        p = Person(firstname='1', lastname='1')
        e = Email(address='addr')
        c = models.Collect(collector_name='toto', facts=[p, e])

        engine_connect = kafka_producers.make_engine_connect()
        engine_connect.produce(
            models.EngineInfo(name='thats my engine name'), flush=True,
        )

        agent_collect = kafka_producers.make_agent_collect()
        # agent_collect.produce(c, flush=True)

        # info_res = kafka_producers.make_agent_broadcast_ping()
        # info_res.produce(models.PingRequest(ping='ping allllllll'), flush=True)

        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)

        # self.producers.agents_info.produce(models.AgentInfoRequest(), flush=True)
        # self.producers.agents_broadcast.produce(models.PingRequest(), flush=True)

    def start(self):

        self.api.start()


engine = SalverEngine()
engine.start()