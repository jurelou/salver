# -*- coding: utf-8 -*-
import time

from salver.facts import Email, Person
from salver.common import models
from salver.config import engine_config
from salver.common.kafka import Consumer
from salver.engine.services import agents, kafka_producers, scan


class SalverEngine:
    def __init__(self):
        common_params = {
            'num_workers': engine_config.kafka.workers_per_topic,
            'num_threads': engine_config.kafka.threads_per_worker,
            'schema_registry_url': engine_config.kafka.schema_registry_url,
            'kafka_config': {
                'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                'group.id': 'engine',
            }
        }
        self.consumers = [
            Consumer(
                topic='agent-connect',
                value_deserializer=models.AgentInfo,
                callback=agents.on_agent_connect,
                **common_params,
            ),
            Consumer(
                topic='agent-disconnect',
                value_deserializer=models.AgentInfo,
                callback=agents.on_agent_disconnect,
                **common_params,
            ),

            Consumer(
                topic='scan',
                value_deserializer=models.Scan,
                callback=scan.OnScan,
                **common_params,
            ),
        ]


    def start(self):
        on_start_called = False

        while True:
            for consumer in self.consumers:
                consumer.start_workers()

            time.sleep(2)
            if not on_start_called:
                self.on_start()
                on_start_called = True

    def on_start(self):
        print('START ENGINE')
        engine_connect = kafka_producers.make_engine_connect()
        engine_connect.produce(
            models.EngineInfo(name='thats my engine name'),
            flush=True,
        )

if __name__ == '__main__':
    engine = SalverEngine()
    engine.start()
