# -*- coding: utf-8 -*-
import os
import time
import threading
from typing import Callable
from queue import Queue
from multiprocessing import Process

from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer

from salver.config import agent_config
from salver.common.avro import make_deserializer
from salver.common.kafka import Consumer, ConsumerCallback
from salver.common import models
from salver.agent.services import collectors

class onping(ConsumerCallback):
    def on_message(self, message):
        print("ON PING", message)

def on_collect(message):
    print("ON AGENT COLLECT", message)

def oninfo(message):
    print("ON INFO", message)

class KafkaConsumers:
    def __init__(self, callback_cls):
        self.consumers = [
            Consumer(
                topic='agent-collect',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.CollectRequest.from_dict,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': 'agents',
                },
                callback_cls=on_collect,
            ),



            Consumer(
                topic='agent-broadcast-ping',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.PingRequest.from_dict,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': 'agentYYY',
                },
                callback_cls=onping,
            ),

            Consumer(
                topic='agent-info',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.AgentInfoRequest.from_dict,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': 'agentYYY',
                },
                callback_cls=oninfo,
            ),

        ]

    def start(self):
        while True:
            for consumer in self.consumers:
                consumer.start_workers()
            # time.sleep(5)
