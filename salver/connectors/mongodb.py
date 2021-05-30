# -*- coding: utf-8 -*-
<<<<<<< HEAD
import pymongo
from loguru import logger

from salver.common import models
from salver.config import connectors_config
from salver.common.kafka import Consumer, ConsumerCallback


class MongoDBCallback(ConsumerCallback):
    def __init__(self):
        self.db = pymongo.MongoClient(connectors_config.mongo.url)[
            connectors_config.mongo.db_name
        ]

=======
from loguru import logger
import pymongo

from salver.common import models
from salver.common.kafka import ConsumerCallback
from salver.config import connectors_config
from salver.common.kafka import Consumer

class MongoDBCallback(ConsumerCallback):
    def __init__(self):
        self.db = pymongo.MongoClient(connectors_config.mongo.url)[connectors_config.mongo.db_name]
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

class OnScan(MongoDBCallback):
    def on_message(self, scan: models.Scan):
        scan.state = models.ScanState.CREATED
        logger.info(f'mongodb connector: Add scan : {scan.external_id}')
        self.db.scans.insert_one(models.Scan.to_dict(scan))

<<<<<<< HEAD

=======
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
class OnCollectCreate(MongoDBCallback):
    def on_message(self, collect: models.Collect):
        collect.state = models.CollectState.CREATED
        logger.info(f'mongodb connector: Add collect: {collect.external_id}')
        self.db.collects.insert_one(models.Collect.to_dict(collect))

<<<<<<< HEAD

class OnCollectDone(MongoDBCallback):
    def on_message(self, collect: models.CollectDone):
        logger.info(f'mongodb connector: collect {collect.collect_id.hex} finished')
        data = collect.dict(exclude={'collect_id'})
        self.db.collects.update_one(
            {'external_id': collect.collect_id.hex},
            {'$set': data},
        )

=======
class OnCollectDone(MongoDBCallback):
    def on_message(self, collect: models.CollectDone):
        logger.info(f'mongodb connector: collect {collect.collect_id.hex} finished')
        data = collect.dict(exclude={"collect_id"})
        self.db.collects.update_one({"external_id": collect.collect_id.hex}, { "$set": data })
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

class OnAgentConnect(MongoDBCallback):
    def on_message(self, agent_info: models.AgentInfo):
        logger.info(f'mongodb connector: add agent {agent_info.name}')
        self.db.agents.insert_one(agent_info.dict())

<<<<<<< HEAD

class OnAgentDisconnect(MongoDBCallback):
    def on_message(self, agent_info: models.AgentInfo):
        logger.info(f'mongodb connector: remove agent {agent_info.name}')
        self.db.agents.delete_one({'name': agent_info.name})
=======
class OnAgentDisconnect(MongoDBCallback):
    def on_message(self, agent_info: models.AgentInfo):
        logger.info(f'mongodb connector: remove agent {agent_info.name}')
        self.db.agents.delete_one({"name": agent_info.name})
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96


def make_consummers():
    common_params = {
<<<<<<< HEAD
        'num_workers': connectors_config.mongo.workers,
        'num_threads': connectors_config.mongo.threads,
        'schema_registry_url': connectors_config.kafka.schema_registry_url,
        'kafka_config': {
            'bootstrap.servers': connectors_config.kafka.bootstrap_servers,
            'group.id': 'mongodb-connector',
=======
        "num_workers": connectors_config.mongo.workers,
        "num_threads": connectors_config.mongo.threads,
        "schema_registry_url": connectors_config.kafka.schema_registry_url,
        "kafka_config": {
            'bootstrap.servers': connectors_config.kafka.bootstrap_servers,
            'group.id': "mongodb-connector",
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
        },
    }
    return [
        Consumer(
<<<<<<< HEAD
            topic='agent-connect',
            value_deserializer=models.AgentInfo,
            callback=OnAgentConnect,
            **common_params,
        ),
        Consumer(
            topic='^collect-create-*',
            schema_name='collect-create',
            value_deserializer=models.Collect,
            callback=OnCollectCreate,
            **common_params,
        ),
        Consumer(
            topic='collect-done',
            value_deserializer=models.CollectDone,
            callback=OnCollectDone,
            **common_params,
        ),
        Consumer(
            topic='scan-create',
            value_deserializer=models.Scan,
            callback=OnScan,
            **common_params,
        ),
        Consumer(
            topic='agent-disconnect',
            value_deserializer=models.AgentInfo,
            callback=OnAgentDisconnect,
            **common_params,
=======
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
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
        ),
    ]
