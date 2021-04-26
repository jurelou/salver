# -*- coding: utf-8 -*-

from multiprocessing import Manager

from salver.common import models
from salver.config import engine_config
from salver.common.kafka import Consumer, ConsumerCallback
from salver.engine.services import kafka_producers

AVAILABLE_AGENTS = Manager().dict()


class AgentInfo(ConsumerCallback):
    def __init__(self):
        # print("NEW", a)
        # self.a = a
        self.agents_broadcast_producer = kafka_producers.make_agent_broadcast_ping()

    def on_message(self, message):
        print('ON AGENT INFO RESPONSE', message)
        AVAILABLE_AGENTS[message.name] = 'ok'
        print(f'available agents: {AVAILABLE_AGENTS}')

        # self.agents_broadcast_producer.produce(
        #     models.PingRequest(ping='enginepinginging'),
        #     flush=True,
        # )


def on_ping(message):
    print('ON PING', message)
    print(f'I HAVE {AVAILABLE_AGENTS}')


class EngineAPI:
    def __init__(self, on_start):
        self.on_start = on_start
        self.on_start_called = False


        from functools import partial
        self.consumers = [
            Consumer(
                topic='agent-info',
                num_workers=engine_config.kafka.workers_per_topic,
                num_threads=engine_config.kafka.threads_per_worker,
                value_deserializer=models.AgentInfo,
                schema_registry_url=engine_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'group.id': 'engine',
                },
                callback=AgentInfo,
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
            if not self.on_start_called:
                self.on_start()
                self.on_start_called = True
            # time.sleep(5)
