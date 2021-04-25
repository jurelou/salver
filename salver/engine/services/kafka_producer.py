# -*- coding: utf-8 -*-
import time
import argparse
from uuid import uuid4

from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer

from salver.config import engine_config
from salver.common.kafka import Producer
from salver.common.models import PingRequest, CollectRequest


class KafkaProducers:
    def __init__(self):

        self.agents_collect = Producer(
            topic='agent-collect',
            value_serializer=CollectRequest.to_dict,
            schema_registry_url=engine_config.kafka.schema_registry_url,
            kafka_config={
                'bootstrap.servers': engine_config.kafka.bootstrap_servers,
            },
        )

        self.agents_broadcast = Producer(
            topic='agent-broadcast-ping',
            value_serializer=PingRequest.to_dict,
            schema_registry_url=engine_config.kafka.schema_registry_url,
            kafka_config={
                'bootstrap.servers': engine_config.kafka.bootstrap_servers,
            },
        )
