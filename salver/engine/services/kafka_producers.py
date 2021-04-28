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


# def make_agent_collect():
#     return Producer(
#         topic='agent-collect',
#         value_serializer=models.CollectRequest,
#         schema_registry_url=engine_config.kafka.schema_registry_url,
#         kafka_config={
#             'bootstrap.servers': engine_config.kafka.bootstrap_servers,
#         },
#     )


def make_engine_connect():
    return Producer(
        topic='engine-connect',
        value_serializer=models.EngineInfo,
        schema_registry_url=engine_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': engine_config.kafka.bootstrap_servers,
        },
    )


def make_agent_collect():
    return Producer(
        topic='agent-collect-create',
        value_serializer=models.Collect,
        schema_registry_url=engine_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': engine_config.kafka.bootstrap_servers,
        },
    )
