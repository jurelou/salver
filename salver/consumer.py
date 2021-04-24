from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer


from schema import *

import threading
import time
from multiprocessing import Process
from queue import Queue
import os



def _process_msg(q, c):
    msg = q.get(timeout=60)

    print("---->", msg.value(), msg.value().listof)
    q.task_done()
    c.commit(msg)



class   Consumer:
    def __init__(self, num_workers, config):
        self.num_workers = num_workers
        self.workers = []
        self.config = config

    @property
    def num_alive(self) -> int:
        return len([w for w in self.workers if w.is_alive()])

    @staticmethod
    def _consume(config):
        print(f"{os.getpid()} Starting consumer group={config['kafka_kwargs']['group.id']}, topic={config['topic']}")
        c = DeserializingConsumer(config['kafka_kwargs'])
        c.subscribe([config['topic']])
        q = Queue(maxsize=config['num_threads'])

        while True:
            # print(f'{os.getpid()} - Waiting for message...')
            try:
                # Check if we should rate limit
                msg = c.poll(1)
                if msg is None:
                    continue
                if msg.error():
                    print(f'{os.getpid()} - Consumer error: {msg.error()}')
                    continue
                q.put(msg)
                t = threading.Thread(target=_process_msg, args=(q, c))
                t.start()
            except Exception as err:
                print(f'{os.getpid()} - Worker terminated., {err}')
                c.close()

    def start_workers(self):
        if self.num_alive == self.num_workers:
            return

        for _ in range(self.num_workers - self.num_alive):
            p = Process(target=self._consume, daemon=True, args=(self.config,))
            p.start()
            self.workers.append(p)
            print(f'Starting worker {p.pid}')


class   AgentConsumer:
    def __init__(self):
        sr_conf = {'url': "http://127.0.0.1:8081"}
        schema_registry_client = SchemaRegistryClient(sr_conf)
        avro_deserializer = AvroDeserializer(schema_str=schema_str, schema_registry_client=schema_registry_client, from_dict=dict_to_user)
        string_deserializer = StringDeserializer('utf_8')

        self.consumers = [
            Consumer(
                num_workers=2,
                    config = {
                        'kafka_kwargs': {
                            'bootstrap.servers': 'localhost:9092',
                            'group.id': 'agents',
                            'auto.offset.reset': 'earliest',
                            'key.deserializer': string_deserializer,
                            'value.deserializer': avro_deserializer,
                            'enable.auto.commit': False,
                        },
                        'topic': 'topic2',
                        "num_threads": 4
                    }
            ),

            Consumer(
                num_workers=2,
                    config = {
                        'kafka_kwargs': {
                            'bootstrap.servers': 'localhost:9092',
                            'group.id': 'agentXXX',
                            'auto.offset.reset': 'earliest',
                            'key.deserializer': string_deserializer,
                            'value.deserializer': avro_deserializer,
                            'enable.auto.commit': False,
                        },
                        'topic': 'topic1',
                        "num_threads": 4
                    }
            )

        ]

    def start(self):
        while True:
            for consumer in self.consumers:
                consumer.start_workers()
            time.sleep(5)


agent = AgentConsumer()
agent.start()
