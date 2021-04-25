# -*- coding: utf-8 -*-
from salver.config import agent_config
from salver.common.kafka import Producer
from salver.common.models import AgentInfo


def make_agent_info_response():
    return Producer(
        topic='agent-info',
        value_serializer=AgentInfo,
        schema_registry_url=agent_config.kafka.schema_registry_url,
        kafka_config={
            'bootstrap.servers': agent_config.kafka.bootstrap_servers,
        },
    )
