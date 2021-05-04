# -*- coding: utf-8 -*-
import os
import types
import signal
import threading
from abc import ABC, abstractmethod
from queue import Queue
from typing import Callable, Optional
from multiprocessing import Process

from loguru import logger
from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer

from salver.common.kafka.serializer import make_deserializer


def _process_msg(q, consumer, callback, topic):
    msg = q.get(timeout=60)
    value = msg.value()
    logger.debug(f'From {topic} got {value}')

    callback(value)

    q.task_done()
    consumer.commit(msg)
    logger.debug(f'Task done {topic}')


class ConsumerCallback(ABC):
    @abstractmethod
    def on_message(self, message):
        pass


class Consumer:
    def __init__(
        self,
        topic,
        value_deserializer,
        num_workers,
        num_threads,
        kafka_config,
        schema_registry_url,
        callback,
        schema_name: Optional[str] = None,
        rate_limit_cb: Optional[Callable] = None,
    ):
        logger.debug(
            f'Create a kafka consumer for topic {topic} with {num_workers} workers and {num_threads} threads',
        )
        self.topic = topic
        if not schema_name:
            schema_name = topic

        self.rate_limit_cb = rate_limit_cb

        self.num_threads = num_threads
        self.num_workers = num_workers

        self.kafka_config = kafka_config
        self.kafka_config = {
            'key.deserializer': StringDeserializer('utf_8'),
            'enable.auto.commit': False,
            'auto.offset.reset': 'latest',
            'value.deserializer': make_deserializer(
                subject=schema_name,
                from_dict=value_deserializer.from_dict,
                schema_registry_url=schema_registry_url,
            ),
        }
        self.kafka_config.update(kafka_config)

        self.workers = []
        self.callback = callback

    @property
    def num_alive(self) -> int:
        return len([w for w in self.workers if w.is_alive()])

    def _consume(self, on_consume):
        if isinstance(on_consume, types.FunctionType):
            callback = on_consume
        else:
            callback_cls = on_consume()
            callback = callback_cls.on_message

        consumer = DeserializingConsumer(self.kafka_config)
        consumer.subscribe([self.topic])
        q = Queue(maxsize=self.num_threads)

        msg = None
        while True:
            try:
                # if self.rate_limit_cb:
                #     self.rate_limit_cb()
                msg = consumer.poll(1)
                if msg is None:
                    continue
                if msg.error():
                    logger.error(f'Worker for topic {self.topic} error: {msg.error()}')
                    continue

                q.put(msg)
                t = threading.Thread(
                    target=_process_msg,
                    args=(q, consumer, callback, self.topic),
                )
                t.start()
            except Exception as err:
                logger.error(f'Worker for topic {self.topic} terminated: {err}')
                logger.error(msg)
                consumer.close()
                break

    def start_workers(self):
        if self.num_alive == self.num_workers:
            return

        for _ in range(self.num_workers - self.num_alive):
            p = Process(target=self._consume, daemon=True, args=(self.callback,))
            p.start()
            self.workers.append(p)
            logger.debug(
                f"Start consumer worker {p.pid} for topic {self.topic} with group {self.kafka_config['group.id']}",
            )
