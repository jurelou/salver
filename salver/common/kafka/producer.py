# -*- coding: utf-8 -*-

from uuid import uuid4

from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer

from salver.common.avro import make_serializer


class Producer:
    def __init__(self, topic, kafka_config, value_serializer, schema_registry_url):
        self.topic = topic

        kafka_config.update(
            {
                'key.serializer': StringSerializer('utf_8'),
                'value.serializer': make_serializer(
                    topic=self.topic,
                    to_dict=value_serializer.to_dict,
                    schema_registry_url=schema_registry_url,
                ),
                'error_cb': lambda x: print('ERRRRRRRRRRR', x),
            },
        )
        self.producer = SerializingProducer(kafka_config)

    @staticmethod
    def _delivery_report(err, msg):
        if err is not None:
            print('Delivery failed for User record {}: {}'.format(msg.key(), err))
            return
        print(
            'record {} successfully produced to {} [{}] at offset {}'.format(
                msg.key(),
                msg.topic(),
                msg.partition(),
                msg.offset(),
            ),
        )

    def produce(self, msg, flush=False):
        self.producer.poll(0.0)
        print(f'Producing records to topic {self.topic}: {msg}')
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
