# -*- coding: utf-8 -*-

from salver.common.collectors import BaseCollector
from salver.common.utils import load_classes
from salver.common.kafka import Producer
from salver.common import models
from salver.config import engine_config

_COMMON_PARAMS = {
        "schema_registry_url": engine_config.kafka.schema_registry_url,
        "kafka_config": {
            'bootstrap.servers': engine_config.kafka.bootstrap_servers,
        },
}
def make_agent_broadcast_ping():
    return Producer(
        topic='agent-broadcast-ping',
        value_serializer=models.PingRequest,
        **_COMMON_PARAMS
    )


def make_engine_connect():
    return Producer(
        topic='engine-connect',
        value_serializer=models.EngineInfo,
        **_COMMON_PARAMS
    )

def make_agent_collect(collector_name: str):
    return Producer(
        topic=f"collect-create-{collector_name}",
        schema_name='collect-create',
        value_serializer=models.Collect,
        **_COMMON_PARAMS
    )


def make_agent_collects():
    collectors = load_classes(
        root_path='salver/agent/collectors',
        parent_class=BaseCollector,
    )
    return {
        c.config['name']: make_agent_collect(c.config['name']) for c in collectors
    }

def make_scan():
    return Producer(
        topic=f"scan",
        value_serializer=models.Scan,
        **_COMMON_PARAMS
    )
