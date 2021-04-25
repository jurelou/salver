# -*- coding: utf-8 -*-
import os
import time
import threading
from queue import Queue
from multiprocessing import Process

from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer

from salver.config import agent_config
from salver.common.avro import make_deserializer
from salver.common.kafka import Consumer
from salver.common.models import PingRequest, CollectRequest
from salver.agent.services import collectors


class KafkaConsummers:
    def __init__(self):
        self.consumers = [
            Consumer(
                topic='agent-collect',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=CollectRequest.from_dict,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': 'agents',
                },
                callback=lambda x: print('CBBB', x),
            ),
            Consumer(
                topic='agent-broadcast-ping',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=PingRequest.from_dict,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': 'agentXXX',
                },
                callback=lambda x: print('CBB222', x),
            ),
        ]

    def start(self):
        while True:
            for consumer in self.consumers:
                consumer.start_workers()
            time.sleep(5)
