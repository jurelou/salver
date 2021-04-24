from salver.common.facts import all_facts
from salver.engine.services.kafka_producer import KafkaProducers
from salver.facts import Person
from salver.common.models.collect import CollectRequest

producer = KafkaProducers()


p = Person(firstname="1", lastname="1")

p2 = Person(firstname="2", lastname="2")


c = CollectRequest(collector_name="toto", facts=["aze", 123, "ert", 32])
c1 = CollectRequest(collector_name="toto111", facts=["123aze", 123123, "123ert", 32123])

producer.agents_collect.produce(c)

producer.agents_broadcast.produce(c1)


producer.agents_collect.flush()
producer.agents_broadcast.flush()

# print(all_facts, Person)