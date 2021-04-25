# -*- coding: utf-8 -*-
from salver.config import agent_config
from salver.common.kafka import Producer
from salver.common.models import AgentInfo


class KafkaProducers:
    def __init__(self):

        self.info_response = Producer(
            topic='agent-info-response',
            value_serializer=AgentInfo.to_dict,
            schema_registry_url=agent_config.kafka.schema_registry_url,
            kafka_config={
                'bootstrap.servers': agent_config.kafka.bootstrap_servers,
            },
        )
