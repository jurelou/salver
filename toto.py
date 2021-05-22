# -*- coding: utf-8 -*-

from salver.common.kafka import Producer
from salver.common import models
from salver.config import engine_config
from salver.facts import Person, Email

p = Person(firstname='1', lastname='1')
p2 = Person(firstname='1', lastname='2')

e = Email(address='addr')
# c = models.Collect(collector_name='dummy-collector', facts=[p, e, p2])

scan_producer = Producer(
    topic=f"scan",
    value_serializer=models.Scan,
    schema_registry_url=engine_config.kafka.schema_registry_url,
    kafka_config = {
        'bootstrap.servers': engine_config.kafka.bootstrap_servers,
    }
)


p = Person(firstname='1', lastname='1')
s = models.Scan(
    scan_type="single_collector",
    config=models.ScanConfig(collector_name="dummy-docker-collector"),
    facts=[p]
)
scan_producer.produce(s, flush=True)
