# -*- coding: utf-8 -*-
import time
import argparse
from uuid import uuid4

from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer


class Producer:
    def __init__(self, topic, kafka_config):
        kafka_config.update({'key.serializer': StringSerializer('utf_8')})
        self.producer = SerializingProducer(kafka_config)
        self.topic = topic

    @staticmethod
    def _delivery_report(err, msg):
        if err is not None:
            print('Delivery failed for User record {}: {}'.format(msg.key(), err))
            return
        print(
            'User record {} successfully produced to {} [{}] at offset {}'.format(
                msg.key(),
                msg.topic(),
                msg.partition(),
                msg.offset(),
            ),
        )

    def produce(self, msg, flush=False):
        print(f'Producing records to topic {self.topic}: {msg}')

        self.producer.poll(0.0)
        self.producer.produce(
            topic=self.topic,
            key=str(uuid4()),
            value=msg,
            on_delivery=self._delivery_report,
        )
        if flush:
            self.flush()

    def flush(self):
        self.producer.flush()
