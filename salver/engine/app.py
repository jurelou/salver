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

        # p = Person(firstname='1', lastname='1')
        # p2 = Person(firstname='1', lastname='2')

        # e = Email(address='addr')
        # c = models.Collect(collector_name='dummy-collector', facts=[p, e, p2])

        # agent_collects = kafka_producers.make_agent_collects()
        # agent_collects['dummy-collector'].produce(c, flush=True)


        # from salver.engine.scans import all_scans

        # scan_producer = kafka_producers.make_scan()
        # p = Person(firstname='1', lastname='1')
        # s = models.Scan(
        #     scan_type="single_collector",
        #     config=models.ScanConfig(collector_name="salut"),
        #     facts=[p]
        # )
        # scan_producer.produce(s, flush=True)
        # print("@@@@@@", all_scans[0].name)
        # info_res = kafka_producers.make_agent_broadcast_ping()
        # info_res.produce(models.PingRequest(ping='ping allllllll'), flush=True)


if __name__ == '__main__':
    engine = SalverEngine()
    engine.start()
