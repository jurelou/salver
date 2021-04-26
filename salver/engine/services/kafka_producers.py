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


def make_agent_collect():
    return Producer(
        topic='agent-collect',
        value_serializer=models.CollectRequest,
        schema_registry_url=engine_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': engine_config.kafka.bootstrap_servers,
        },
    )


def make_request_agent_info():
    return Producer(
        topic='request-agent-info',
        value_serializer=models.AgentInfoRequest,
        schema_registry_url=engine_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': engine_config.kafka.bootstrap_servers,
        },
    )
