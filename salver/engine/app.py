# -*- coding: utf-8 -*-
from salver.facts import Email, Person
from salver.common.facts import all_facts
from salver.common.models.collect import CollectRequest
from salver.engine.services.kafka_producer import KafkaProducers

producer = KafkaProducers()


p = Person(firstname='1', lastname='1')
e = Email(address='addr')

p2 = Person(firstname='2', lastname='2')
e2 = Email(address='addr22é')

c = CollectRequest(collector_name='toto', facts=[p, e])
c1 = CollectRequest(collector_name='toto111', facts=[p2, e2])

producer.agents_collect.produce(c)

producer.agents_broadcast.produce(c1)


producer.agents_collect.flush()
producer.agents_broadcast.flush()

# print(all_facts, Person)
