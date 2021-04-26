# -*- coding: utf-8 -*-

from uuid import uuid4

from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer

from salver.common.avro import make_serializer
from loguru import logger

class Producer:
    def __init__(self, topic, kafka_config, value_serializer, schema_registry_url):
        self.topic = topic
        logger.debug(f'Create kafka producer for topic {self.topic}')
        kafka_config.update(
            {
                'key.serializer': StringSerializer('utf_8'),
                'value.serializer': make_serializer(
                    topic=self.topic,
                    to_dict=value_serializer.to_dict,
                    schema_registry_url=schema_registry_url,
                ),
                'error_cb': lambda err: logger.error(f'Producer for {topic} error: {err}'),
            },
        )
        self.producer = SerializingProducer(kafka_config)

    @staticmethod
    def _delivery_report(err, msg):
        if err is not None:
            logger.error(f'Delivery failed for {msg.key()}: {err}')
            return
        logger.debug(f'Produced {str(msg.key())} to {msg.topic()}')
                # msg.key(),
                # msg.topic(),
                # msg.partition(),
                # msg.offset(),

    def produce(self, msg, flush=False):
        self.producer.poll(0.0)
        msg_id = uuid4().hex
        logger.debug(f'Producing {msg_id} to {self.topic}: {msg}')
        self.producer.produce(
            topic=self.topic,
            key=msg_id,
            value=msg,
            on_delivery=self._delivery_report,
        )
        if flush:
            self.flush()

    def flush(self):
        logger.debug(f'Flush producer for {self.topic}')
        self.producer.flush()
