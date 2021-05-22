# -*- coding: utf-8 -*-
from salver.config import agent_config
from salver.common.kafka import Producer
from salver.common.models import AgentInfo, CollectResponse


def make_agent_connect():
    return Producer(
        topic='agent-connect',
        value_serializer=AgentInfo,
        schema_registry_url=agent_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': agent_config.kafka.bootstrap_servers,
        },
    )

def make_collect_response():
    return Producer(
        topic='response-collect',
        value_serializer=CollectResponse,
        schema_registry_url=agent_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': agent_config.kafka.bootstrap_servers,
        },
    )


def make_agent_disconnect():
    return Producer(
        topic='agent-disconnect',
        value_serializer=AgentInfo,
        schema_registry_url=agent_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': agent_config.kafka.bootstrap_servers,
        },
    )
