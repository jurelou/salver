# -*- coding: utf-8 -*-

<<<<<<< HEAD
from salver.common import models
from salver.config import engine_config
from salver.common.kafka import Producer

from .collectors import all_collectors

_COMMON_PARAMS = {
    'schema_registry_url': engine_config.kafka.schema_registry_url,
    'kafka_config': {
        'bootstrap.servers': engine_config.kafka.bootstrap_servers,
    },
}

=======
from salver.common.kafka import Producer
from salver.common import models
from salver.config import engine_config
from .collectors import all_collectors
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

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
<<<<<<< HEAD
        **_COMMON_PARAMS,
=======
        **_COMMON_PARAMS
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
    )


def make_engine_connect():
    return Producer(
        topic='engine-connect',
        value_serializer=models.EngineInfo,
<<<<<<< HEAD
        **_COMMON_PARAMS,
    )


def make_agent_collect(collector_name: str):
    return Producer(
        topic=f'collect-create-{collector_name}',
        schema_name='collect-create',
        value_serializer=models.Collect,
        **_COMMON_PARAMS,
=======
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
    return {
        c.config['name']: make_agent_collect(c.config['name']) for c in all_collectors
    }

def make_scan():
    return Producer(
        topic=f"scan",
        value_serializer=models.Scan,
        **_COMMON_PARAMS
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
    )


def make_agent_collects():
    return {
        c.config['name']: make_agent_collect(c.config['name']) for c in all_collectors
    }


def make_scan():
    return Producer(topic=f'scan', value_serializer=models.Scan, **_COMMON_PARAMS)
