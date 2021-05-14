# -*- coding: utf-8 -*-
from loguru import logger
import pymongo

from salver.common import models
from salver.common.kafka import ConsumerCallback
from salver.config import connectors_config
from salver.common.kafka import Consumer

class MongoDBCallback(ConsumerCallback):
    def __init__(self):
        self.db = pymongo.MongoClient(connectors_config.mongo.url)[connectors_config.mongo.db_name]

class OnCollectCreate(MongoDBCallback):
    def on_message(self, collect: models.Collect):
        collect.state = models.CollectState.CREATED
        logger.info(f'mongodb connector: Add collect item: {collect}')
        self.db.collects.insert_one(models.Collect.to_dict(collect))

class OnAgentConnect(MongoDBCallback):
    def on_message(self, agent_info: models.AgentInfo):
        logger.info(f'mongodb connector: add agent {agent_info.name}')
        self.db.agents.insert_one(agent_info.dict())

class OnAgentDisconnect(MongoDBCallback):
    def on_message(self, agent_info: models.AgentInfo):
        logger.info(f'mongodb connector: remove agent {agent_info.name}')
        self.db.agents.delete_one({"name": agent_info.name})


def make_consummers():
    common_params = {
        "num_workers": connectors_config.mongo.workers,
        "num_threads": connectors_config.mongo.threads,
        "schema_registry_url": connectors_config.kafka.schema_registry_url,
        "kafka_config": {
            'bootstrap.servers': connectors_config.kafka.bootstrap_servers,
            'group.id': "mongodb-connector",
        },
    }
    return [
        # Consumer(
        #         topic='^agent-collect-*',
        #         schema_name='agent-collect-create',
        #         value_deserializer=models.Collect,
        #         callback=OnCollectCreate,
        #         **common_params
        # ),
        Consumer(
                topic='agent-connect',
                value_deserializer=models.AgentInfo,
                callback=OnAgentConnect,
                **common_params
        ),
        Consumer(
                topic='agent-disconnect',
                value_deserializer=models.AgentInfo,
                callback=OnAgentDisconnect,
                **common_params
        ),
    ]
