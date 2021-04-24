# -*- coding: utf-8 -*-
import os
import time
import threading
from queue import Queue
from multiprocessing import Process

from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer

from salver.config import agent_config
from salver.common.avro import make_deserializer
from salver.common.models import PingRequest, CollectRequest


def _process_msg(q, consumer, callback):
    msg = q.get(timeout=60)

    callback(msg.value())

    q.task_done()
    consumer.commit(msg)


class Consumer:
    def __init__(self, topic, num_workers, num_threads, kafka_config, callback):
        self.topic = topic
        self.num_threads = num_threads
        self.num_workers = num_workers

        self.kafka_config = kafka_config
        self.kafka_config = {
            'key.deserializer': StringDeserializer('utf_8'),
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest',
        }
        self.kafka_config.update(kafka_config)

        self.workers = []
        self.callback = callback

    @property
    def num_alive(self) -> int:
        return len([w for w in self.workers if w.is_alive()])

    def _consume(self):
        print(
            f"{os.getpid()} Starting consumer group={self.kafka_config['group.id']}, topic={self.topic}",
        )
        consumer = DeserializingConsumer(self.kafka_config)
        consumer.subscribe([self.topic])
        q = Queue(maxsize=self.num_threads)

        while True:
            # print(f'{os.getpid()} - Waiting for message...')
            try:
                # Check if we should rate limit
                msg = consumer.poll(1)
                if msg is None:
                    continue
                if msg.error():
                    print(f'{os.getpid()} - Consumer error: {msg.error()}')
                    continue
                q.put(msg)
                t = threading.Thread(
                    target=_process_msg, args=(q, consumer, self.callback),
                )
                t.start()
            except Exception as err:
                print(f'{os.getpid()} - Worker terminated., {err}')
                consumer.close()
                break

    def start_workers(self):
        if self.num_alive == self.num_workers:
            return

        for _ in range(self.num_workers - self.num_alive):
            p = Process(
                target=self._consume,
                daemon=True,
            )
            p.start()
            self.workers.append(p)
            print(f'Starting worker {p.pid}')
