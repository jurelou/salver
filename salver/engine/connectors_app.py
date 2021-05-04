# -*- coding: utf-8 -*-
import time

from salver.common import models
from salver.config import engine_config
from salver.common.kafka import Consumer
from salver.engine.connectors import OnCollectCreate


def make_connectors():
    group_id = 'salver-connector'
    consumers = []

    if engine_config.connectors.mongo.enabled:
        consumers.append(
            Consumer(
                topic='^agent-collect-*',
                schema_name='agent-collect-create',
                num_workers=engine_config.connectors.mongo.workers,
                num_threads=engine_config.connectors.mongo.threads,
                value_deserializer=models.Collect,
                schema_registry_url=engine_config.kafka.schema_registry_url,
                kafka_config={
                    'bootstrap.servers': engine_config.kafka.bootstrap_servers,
                    'group.id': group_id,
                },
                callback=OnCollectCreate,
            ),
        )
    return consumers


if __name__ == '__main__':
    connectors = make_connectors()
    while True:
        for connector in connectors:
            connector.start_workers()
        time.sleep(5)
