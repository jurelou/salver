# -*- coding: utf-8 -*-


from salver.common import models
from salver.config import agent_config
from salver.common.kafka import Consumer, ConsumerCallback
from salver.agent.services import kafka_producers


class OnPing(ConsumerCallback):
    def on_message(self, message):
        print('ON PING', message)


class OnAgentInfo(ConsumerCallback):
    def __init__(self):
        self.agent_info_producer = kafka_producers.make_agent_info_response()

    def on_message(self, agent_info_request):
        print('ON AGENT INFO', agent_info_request)
        self.agent_info_producer.produce(
            models.AgentInfo(name='init agent because asked ....'), flush=True,
        )


def on_collect(message):
    print('ON AGENT COLLECT', message)


class AgentAPI:
    def __init__(self, agent_name: str):
        print('CREATE AGENT API')
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
                topic='agent-info-request',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.AgentInfoRequest,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': agent_name,
                },
                callback=OnAgentInfo,
            ),
        ]

    def start(self):
        while True:
            for consumer in self.consumers:
                consumer.start_workers()
            # time.sleep(5)
