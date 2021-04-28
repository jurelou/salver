# -*- coding: utf-8 -*-


import sys
import signal
from functools import partial

from loguru import logger

from salver.common import models
from salver.config import agent_config
from salver.common.kafka import Consumer, ConsumerCallback
from salver.agent.services import kafka_producers


class OnPing(ConsumerCallback):
    def on_message(self, message):
        logger.info(f'Got ping: {message}')


class OnEngineConnect(ConsumerCallback):
    def __init__(self, agent_info):
        self.agent_connect = kafka_producers.make_agent_connect()
        self.agent_info = agent_info

    def on_message(self, agent_info_request):
        logger.info(f'Got engine connect: {agent_info_request}')
        self.agent_connect.produce(self.agent_info, flush=True)


def on_collect(message):
    logger.info(f'Got agent collect: {message}')


class AgentAPI:
    def __init__(self, agent_info: models.AgentInfo):
        self.agent_info = agent_info

        self.consumers = [
            Consumer(
                topic='agent-collect-create',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.Collect,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': 'agents',
                },
                callback=on_collect,
            ),
            Consumer(
                topic='agent-broadcast-ping',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.PingRequest,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': agent_info.name,
                },
                callback=OnPing,
            ),
            Consumer(
                topic='engine-connect',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.EngineInfo,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': agent_info.name,
                },
                callback=partial(OnEngineConnect, agent_info),
            ),
        ]

    def start(self):
        while True:
            for consumer in self.consumers:
                consumer.start_workers()
        # time.sleep(5)

    def stop(self):
        pass
