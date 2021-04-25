# -*- coding: utf-8 -*-
from salver.agent.services.kafka_consumers import KafkaConsumers
from salver.agent.services.kafka_producers import KafkaProducers

from salver.agent.api import AgentAPI
from salver.common import models


class   SalverAgent:
    def __init__(self):
        self.producers = KafkaProducers()
        self.api = AgentAPI()

        # self.api = AgentAPI(producers=self.producers)
        # self.consumers = KafkaConsumers(callback_cls=AgentAPI)

    def start(self):
        self.producers.info_response.produce(models.AgentInfo(name="fromhere"), flush=True)

        self.api.start()


agent = SalverAgent()
agent.start()