# -*- coding: utf-8 -*-
from multiprocessing import Manager, Process
from multiprocessing.managers import BaseManager

from salver.common import models
from salver.config import engine_config
from salver.common.kafka import Consumer, ConsumerCallback
from salver.engine.services import kafka_producers


class OnInfoResponse(ConsumerCallback):
    def __init__(self):
        self.agents_broadcast_producer = kafka_producers.make_agent_broadcast_ping()

    def on_message(self, message):
        print('ON INFO RESPONSE', message)
        self.agents_broadcast_producer.produce(
            models.PingRequest(ping='enginepinginging'),
            flush=True,
        )


def on_ping(message):
    print('ON PING', message)


class EngineAPI:
    def __init__(self):
        self.consumers = [
            Consumer(
                topic='agent-info-response',
                num_workers=engine_config.kafka.workers_per_topic,
                num_threads=engine_config.kafka.threads_per_worker,
                value_deserializer=models.AgentInfo,
                schema_registry_url=engine_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'group.id': 'engine',
                },
                callback=OnInfoResponse,
            ),
            Consumer(
                topic='agent-broadcast-ping',
                num_workers=engine_config.kafka.workers_per_topic,
                num_threads=engine_config.kafka.threads_per_worker,
                value_deserializer=models.PingRequest,
                schema_registry_url=engine_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'group.id': 'agentENGINE',
                },
                callback=on_ping,
            ),
        ]

    def start(self):
        while True:
            for consumer in self.consumers:
                consumer.start_workers()
            # time.sleep(5)
