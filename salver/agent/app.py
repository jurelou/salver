# -*- coding: utf-8 -*-
import sys
import socket
from uuid import uuid4
from signal import SIGTERM, signal
from functools import partial

from loguru import logger

from salver.common import models
from salver.config import agent_config
from salver.common.kafka import Consumer, ConsumerCallback

# from salver.agent.api import AgentAPI
from salver.agent.services import collectors, kafka_producers


class OnEngineConnect(ConsumerCallback):
    def __init__(self, agent_info):
        self.agent_connect = kafka_producers.make_agent_connect()
        self.agent_info = agent_info

    def on_message(self, agent_info_request):
        logger.info(f'Got engine connect: {agent_info_request}')
        self.agent_connect.produce(self.agent_info, flush=True)


def on_collect(message):
    logger.info(f'Got agent collect: {message}')


class SalverAgent:
    def __init__(self):
        self.name = f'agent-{socket.getfqdn()}-{uuid4().hex[:4]}'
        all_collectors = [
            models.Collector(name=c_name, enabled=c_config['enabled'])
            for c_name, c_config in collectors.ALL_COLLECTORS.items()
        ]
        self.agent_info = models.AgentInfo(name=self.name, collectors=all_collectors)

        common_settings = {
            'num_workers': agent_config.kafka.workers_per_topic,
            'num_threads': agent_config.kafka.threads_per_worker,
            'schema_registry_url': agent_config.kafka.schema_registry_url,
        }
        self.consumers = [
            Consumer(
                topic='agent-collect-create',
                value_deserializer=models.Collect,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': 'agents',
                },
                callback=on_collect,
                **common_settings,
            ),
            Consumer(
                topic='engine-connect',
                value_deserializer=models.EngineInfo,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': self.agent_info.name,
                },
                callback=partial(OnEngineConnect, self.agent_info),
                **common_settings,
            ),
        ]

    def start(self):
        logger.info(f'Starting agent {self.name}')

        agent_connect = kafka_producers.make_agent_connect()
        agent_connect.produce(self.agent_info, flush=True)

        agent_disconnect = kafka_producers.make_agent_disconnect()

        try:
            while True:
                for consumer in self.consumers:
                    consumer.start_workers()
        except KeyboardInterrupt:
            logger.warning('quitting')
            agent_disconnect.produce(self.agent_info, flush=True)


if __name__ == '__main__':
    agent = SalverAgent()
    agent.start()
