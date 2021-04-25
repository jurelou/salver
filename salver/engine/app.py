# # -*- coding: utf-8 -*-
# from salver.facts import Email, Person
# from salver.common.facts import all_facts
# from salver.common.models import PingRequest, CollectRequest
# from salver.engine.services.kafka_producer import KafkaProducers

# producer = KafkaProducers()


# p = Person(firstname='1', lastname='1')
# e = Email(address='addr')

# p2 = Person(firstname='2', lastname='2')
# e2 = Email(address='addr22é')

# c = CollectRequest(collector_name='toto', facts=[p, e])
# c1 = CollectRequest(collector_name='toto111', facts=[p2, e2])

# producer.agents_collect.produce(c)

# producer.agents_broadcast.produce(PingRequest())


# producer.agents_collect.flush()
# producer.agents_broadcast.flush()

# -*- coding: utf-8 -*-
from salver.engine.services.kafka_consumers import KafkaConsumers
from salver.engine.services.kafka_producers import KafkaProducers
from salver.engine.api import EngineAPI
from salver.common import models
from salver.facts import Person, Email

from salver.common.kafka.topic import Topic


class   SalverEngine:
    def __init__(self):
        pass
        # self.producers = KafkaProducers()
        self.api = EngineAPI()
        # self.consumers = KafkaConsumers(callback_cls=EngineAPI)

    def start(self):

        p = Person(firstname='1', lastname='1')
        e = Email(address='addr')
        c = models.CollectRequest(collector_name='toto', facts=[p, e])

        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)
        # self.producers.agents_collect.produce(c, flush=True)

        # self.producers.agents_info.produce(models.AgentInfoRequest(), flush=True)
        # self.producers.agents_broadcast.produce(models.PingRequest(), flush=True)

        # self.consumers.start()


engine = SalverEngine()
engine.start()