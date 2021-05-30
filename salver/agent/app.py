# -*- coding: utf-8 -*-
import sys
import socket
from uuid import uuid4
from signal import SIGTERM, signal
from functools import partial

from loguru import logger

from salver.agent import tasks
from salver.common import models
from salver.config import agent_config
from salver.common.kafka import Consumer

# from salver.agent.api import AgentAPI
from salver.agent.services import collectors, kafka_producers

ALL_COLLECTORS = collectors.build()


class SalverAgent:
    def __init__(self):
        self.name = f'agent-{socket.getfqdn()}-{uuid4().hex[:4]}'
        all_collectors = [
<<<<<<< HEAD
            models.Collector(
                name=c_name,
                enabled=c_config['enabled'],
                allowed_input=c_config['allowed_input'],
            )
=======
            models.Collector(name=c_name, enabled=c_config['enabled'], allowed_input=c_config['allowed_input'])
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
            for c_name, c_config in ALL_COLLECTORS.items()
        ]
        enabled_collectors = {
            name: c['instance'] for name, c in ALL_COLLECTORS.items() if c['enabled']
        }
        self.agent_info = models.AgentInfo(name=self.name, collectors=all_collectors)

        common_settings = {
            'num_workers': agent_config.kafka.workers_per_topic,
            'num_threads': agent_config.kafka.threads_per_worker,
            'schema_registry_url': agent_config.kafka.schema_registry_url,
        }
        self.consumers = [
            Consumer(
                topic='engine-connect',
                value_deserializer=models.EngineInfo,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': self.agent_info.name,
                },
                callback=partial(tasks.OnEngineConnect, self.agent_info),
                **common_settings,
            ),
        ]
        for collector_name, collector_config in ALL_COLLECTORS.items():
            limiter = collector_config['instance'].limiter
            if limiter:
                limiter = limiter.rate_limit

            self.consumers.append(
                Consumer(
                    topic=f'collect-create-{collector_name}',
                    schema_name='collect-create',
                    value_deserializer=models.Collect,
                    kafka_config={
                        'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                        'group.id': 'agents',
                    },
                    callback=partial(tasks.OnCollect, enabled_collectors),
                    rate_limit_cb=limiter,
                    **common_settings,
                ),
            )

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
            logger.warning('Quitting, keyboard interrupt')
            agent_disconnect.produce(self.agent_info, flush=True)


if __name__ == '__main__':
    agent = SalverAgent()
    agent.start()
