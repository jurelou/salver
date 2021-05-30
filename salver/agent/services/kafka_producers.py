# -*- coding: utf-8 -*-
from salver.config import agent_config
from salver.common.kafka import Producer
from salver.common import models

def make_error():
    return Producer(
        topic='error',
        value_serializer=models.Error,
        schema_registry_url=agent_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': agent_config.kafka.bootstrap_servers,
        },
    )


def make_agent_connect():
    return Producer(
        topic='agent-connect',
        value_serializer=models.AgentInfo,
        schema_registry_url=agent_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': agent_config.kafka.bootstrap_servers,
        },
    )

def make_collect_response():
    return Producer(
        topic='collect-response',
        value_serializer=models.CollectResponse,
        schema_registry_url=agent_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': agent_config.kafka.bootstrap_servers,
        },
    )

def make_collect_done():
    return Producer(
        topic='collect-done',
        value_serializer=models.CollectDone,
        schema_registry_url=agent_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': agent_config.kafka.bootstrap_servers,
        },
    )

def make_agent_disconnect():
    return Producer(
        topic='agent-disconnect',
        value_serializer=models.AgentInfo,
        schema_registry_url=agent_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': agent_config.kafka.bootstrap_servers,
        },
    )
