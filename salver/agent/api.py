from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

from salver.common import models
from salver.config import agent_config
from salver.common.kafka import Producer, Consumer, ConsumerCallback


class onping(ConsumerCallback):
    def on_message(self, message):
        print("ON PING", message)

def on_collect(message):
    print("ON AGENT COLLECT", message)

def oninfo(message):
    print("ON INFO", message)

class AgentAPI:

    def __init__(self):
        print("CREATE AGENT API")

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
                    'group.id': 'agentYYY',
                },
                callback=onping,
            ),

            Consumer(
                topic='agent-info',
                num_workers=agent_config.kafka.workers_per_topic,
                num_threads=agent_config.kafka.threads_per_worker,
                value_deserializer=models.AgentInfoRequest,
                schema_registry_url=agent_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': agent_config.kafka.bootstrap_servers,
                    'group.id': 'agentYYY',
                },
                callback=oninfo,
            ),

        ]

    def start(self):
        while True:
            for consumer in self.consumers:
                consumer.start_workers()
            # time.sleep(5)