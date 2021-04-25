# -*- coding: utf-8 -*-
import os
import time
import threading
from typing import Callable


from salver.config import engine_config
from salver.common.kafka import Consumer, ConsumerCallback
from salver.common import models

from .kafka_producers import KafkaProducers

class OnInfoResponse(ConsumerCallback):
    def __init__(self):
        self.producers = KafkaProducers()

    def on_message(self, message):
        print("ON INFO RESPONSE", message)
        self.producers.agents_broadcast.produce(models.PingRequest(ping="enginepinginging"), flush=True)

def on_ping(message):
    print("ON PING", message)

class KafkaConsumers:
    def __init__(self, callback_cls):
        self.consumers = [

            Consumer(
                topic='agent-info-response',
                num_workers=engine_config.kafka.workers_per_topic,
                num_threads=engine_config.kafka.threads_per_worker,
                value_deserializer=models.AgentInfo.from_dict,
                schema_registry_url=engine_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'group.id': 'engine',
                },
                callback_cls=OnInfoResponse
            ),


            Consumer(
                topic='agent-broadcast-ping',
                num_workers=engine_config.kafka.workers_per_topic,
                num_threads=engine_config.kafka.threads_per_worker,
                value_deserializer=models.PingRequest.from_dict,
                schema_registry_url=engine_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'group.id': 'agentENGINE',
                },
                callback_cls=on_ping

            ),


        ]

    def start(self):
        while True:
            for consumer in self.consumers:
                consumer.start_workers()
            # time.sleep(5)
