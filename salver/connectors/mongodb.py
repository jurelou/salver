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

class OnScan(MongoDBCallback):
    def on_message(self, scan: models.Scan):
        scan.state = models.ScanState.CREATED
        logger.info(f'mongodb connector: Add scan : {scan.external_id}')
        self.db.scans.insert_one(models.Scan.to_dict(scan))

class OnCollectCreate(MongoDBCallback):
    def on_message(self, collect: models.Collect):
        collect.state = models.CollectState.CREATED
        logger.info(f'mongodb connector: Add collect: {collect.external_id}')
        self.db.collects.insert_one(models.Collect.to_dict(collect))

class OnCollectDone(MongoDBCallback):
    def on_message(self, collect: models.CollectDone):
        logger.info(f'mongodb connector: collect {collect.collect_id.hex} finished')
        data = collect.dict(exclude={"collect_id"})
        self.db.collects.update_one({"external_id": collect.collect_id.hex}, { "$set": data })

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
        Consumer(
                topic='agent-connect',
                value_deserializer=models.AgentInfo,
                callback=OnAgentConnect,
                **common_params 
        ),
        Consumer(
                    topic='^collect-create-*',
                    schema_name='collect-create',
                    value_deserializer=models.Collect,
                    callback=OnCollectCreate,
                    **common_params
        ),
        Consumer(
                    topic='collect-done',
                    value_deserializer=models.CollectDone,
                    callback=OnCollectDone,
                    **common_params
        ),
        Consumer(
                topic='scan',
                value_deserializer=models.Scan,
                callback=OnScan,
                **common_params
        ),
        Consumer(
                topic='agent-disconnect',
                value_deserializer=models.AgentInfo,
                callback=OnAgentDisconnect,
                **common_params
        ),
    ]
