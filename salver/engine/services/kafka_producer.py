# -*- coding: utf-8 -*-
import argparse
from uuid import uuid4

from six.moves import input

from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import time

from schema import *

from salver.config import engine_config

from salver.common.models.collect import CollectRequest
from salver.common.avro import make_serializer



class   Producer:
    def __init__(self, config, topic):
        self.producer = SerializingProducer(config)
        self.topic = topic

    @staticmethod
    def _delivery_report(err, msg):
        if err is not None:
            print('Delivery failed for User record {}: {}'.format(msg.key(), err))
            return
        print(
            'User record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset(),
            ),
        )


    def produce(self, msg, flush=False):
        print(f'Producing ecords to topic {self.topic}: {msg}')

        self.producer.poll(0.0)
        self.producer.produce(
            topic=self.topic, key=str(uuid4()), value=msg,
            on_delivery=self._delivery_report,
        )
        if flush:
            self.flush()

    def flush(self):
        self.producer.flush()

class   KafkaProducers:
    def __init__(self):
        string_serializer = StringSerializer('utf_8')

        self.agents_collect = Producer(
                config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'key.serializer': string_serializer,
                    'value.serializer': make_serializer(
                        topic="agent-collect",
                        to_dict=CollectRequest.to_dict,
                        schema_registry_url=engine_config.kafka.schema_registry_url
                    )
                },
                topic='agent-collect',
        )

        self.agents_broadcast = Producer(
                config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'key.serializer': string_serializer,
                    'value.serializer': make_serializer(
                        topic="agent-broadcast",
                        to_dict=CollectRequest.to_dict,
                        schema_registry_url=engine_config.kafka.schema_registry_url
                    )
                },
                topic='agent-broadcast',
        )
