# -*- coding: utf-8 -*-


from salver.common import models
from salver.config import agent_config
from salver.common.kafka import Consumer, ConsumerCallback
from salver.agent.services import kafka_producers
from functools import partial
from loguru import logger


class OnPing(ConsumerCallback):
    def on_message(self, message):
        logger.info(f'Got ping: {message}')


class OnAgentInfo(ConsumerCallback):
    def __init__(self, agent_name):
        self.agent_info_producer = kafka_producers.make_agent_info_response()
        self.agent_name = agent_name

    def on_message(self, agent_info_request):
        logger.info(f'Got agent info: {agent_info_request}')
        self.agent_info_producer.produce(
            models.AgentInfo(name=self.agent_name), flush=True,
        )


def on_collect(message):
    logger.info(f'Got agent collect: {message}')


class AgentAPI:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

        self.consumers = [
            Consumer(
                topic='agent-collect',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.CollectRequest,
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
                    'group.id': agent_name,
                },
                callback=OnPing,
            ),
            Consumer(
                topic='request-agent-info',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.AgentInfoRequest,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': agent_name,
                },
                callback=partial(OnAgentInfo, self.agent_name),
            ),
        ]

    def start(self):
        while True:
            for consumer in self.consumers:
                consumer.start_workers()
            # time.sleep(5)
