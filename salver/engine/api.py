# -*- coding: utf-8 -*-


from salver.common import models
from salver.config import engine_config
from salver.common.kafka import Consumer, ConsumerCallback
from salver.engine.services.agents import OnAgentConnect, on_agent_disconnect


def on_ping(message):
    print('ON PING', message)
    # print(f'I HAVE {AVAILABLE_AGENTS}')


class EngineAPI:
    def __init__(self, on_start):
        self.on_start = on_start
        self.on_start_called = False

        self.consumers = [
            Consumer(
                topic='agent-connect',
                num_workers=engine_config.kafka.workers_per_topic,
                num_threads=engine_config.kafka.threads_per_worker,
                value_deserializer=models.AgentInfo,
                schema_registry_url=engine_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'group.id': 'engine',
                },
                callback=OnAgentConnect,
            ),
            Consumer(
                topic='agent-broadcast-ping',
                num_workers=engine_config.kafka.workers_per_topic,
                num_threads=engine_config.kafka.threads_per_worker,
                value_deserializer=models.PingRequest,
                schema_registry_url=engine_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'group.id': 'engine',
                },
                callback=on_ping,
            ),
            Consumer(
                topic='agent-disconnect',
                num_workers=engine_config.kafka.workers_per_topic,
                num_threads=engine_config.kafka.threads_per_worker,
                value_deserializer=models.AgentInfo,
                schema_registry_url=engine_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'group.id': 'engine',
                },
                callback=on_agent_disconnect,
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
