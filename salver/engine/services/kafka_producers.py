# -*- coding: utf-8 -*-


from salver.common import models
from salver.config import engine_config
from salver.common.kafka import Producer


def make_agent_broadcast_ping():
    return Producer(
        topic='agent-broadcast-ping',
        value_serializer=models.PingRequest,
        schema_registry_url=engine_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': engine_config.kafka.bootstrap_servers,
        },
    )


def make_engine_connect():
    return Producer(
        topic='engine-connect',
        value_serializer=models.EngineInfo,
        schema_registry_url=engine_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': engine_config.kafka.bootstrap_servers,
        },
    )


from salver.common.utils import load_classes
from salver.common.collectors import BaseCollector


def make_agent_collects():
    collectors = load_classes(
        root_path='salver/agent/collectors',
        parent_class=BaseCollector,
    )

    return {
        c.config['name']: Producer(
            topic=f"agent-collect-{c.config['name']}",
            schema_name='agent-collect-create',
            value_serializer=models.Collect,
            schema_registry_url=engine_config.kafka.schema_registry_url,
            kafka_config={
                'bootstrap.servers': engine_config.kafka.bootstrap_servers,
            },
        )
        for c in collectors
    }
