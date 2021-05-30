# -*- coding: utf-8 -*-
import sys
import json
import time

from confluent_kafka.admin import NewTopic, AdminClient
from confluent_kafka.schema_registry import Schema, SchemaRegistryClient

from salver.common import models
from salver.common.facts import all_facts
from salver.common.utils import load_classes
from salver.agent.services import collectors
from salver.common.collectors import BaseCollector

<<<<<<< HEAD
=======

>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
collector_modules = load_classes(
    root_path='salver/agent/collectors',
    parent_class=BaseCollector,
)

<<<<<<< HEAD
schema_registry = 'http://localhost:8081'
kafka_bootstrap = 'localhost:9092'
=======
schema_registry = "http://localhost:8081"
kafka_bootstrap = "localhost:9092"
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

topics = [
    'agent-broadcast-ping',
    'engine-connect',
    'agent-disconnect',
    'agent-connect',
<<<<<<< HEAD
    'scan-create',
    'error',
    'collect-result',
=======

    'scan',
    'error',

    'collect-response',
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
    'collect-done',
]

topics.extend([f"collect-create-{c.config['name']}" for c in collector_modules])


admin_client = AdminClient({'bootstrap.servers': kafka_bootstrap})
shema_registry_client = SchemaRegistryClient({'url': schema_registry})


def delete_topics():
    fs = admin_client.delete_topics(topics)
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f'Topic {topic} deleted')
        except Exception as e:
<<<<<<< HEAD
            pass
=======
            print('Failed to delete topic {}: {}'.format(topic, e))
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
    time.sleep(2)  # For some reasons changes are asynchronous ....


def create_topics():
    new_topics = [
        NewTopic(topic, num_partitions=3, replication_factor=1) for topic in topics
    ]
    fs = admin_client.create_topics(new_topics)

    # Wait for each operation to finish.
    for topic, f in fs.items():
        try:
            res = f.result()  # The result itself is None
            print(f'Topic {topic} created: {res}')
        except Exception as e:
            print('Failed to create topic {}: {}'.format(topic, e))


delete_topics()
create_topics()


def remove_schemas():
    for subject in shema_registry_client.get_subjects():
        print('Remobe schema subject', subject)
        shema_registry_client.delete_subject(subject)


def create_schemas():

    shema_registry_client.register_schema(
        'scan-create',
        Schema(schema_str=json.dumps(models.Scan.schema()), schema_type='JSON'),
    )
    shema_registry_client.register_schema(
        'collect-create',
        Schema(schema_str=json.dumps(models.Collect.schema()), schema_type='JSON'),
    )

    shema_registry_client.register_schema(
        'BaseFact',
        Schema(schema_str=json.dumps(models.BaseFact.schema()), schema_type='JSON'),
    )
    shema_registry_client.register_schema(
<<<<<<< HEAD
        'error',
        Schema(schema_str=json.dumps(models.Error.schema()), schema_type='JSON'),
    )
    shema_registry_client.register_schema(
        'collect-done',
        Schema(schema_str=json.dumps(models.CollectDone.schema()), schema_type='JSON'),
    )
    shema_registry_client.register_schema(
        'collect-result',
        Schema(
            schema_str=json.dumps(models.CollectResult.schema()),
            schema_type='JSON',
        ),
=======
        'collect-create',
        Schema(schema_str=json.dumps(models.Collect.schema()), schema_type='JSON'),
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
    )
    shema_registry_client.register_schema(
        'error',
        Schema(schema_str=json.dumps(models.Error.schema()), schema_type='JSON'),
    )
    shema_registry_client.register_schema(
        'collect-done',
        Schema(schema_str=json.dumps(models.CollectDone.schema()), schema_type='JSON'),
    )
    shema_registry_client.register_schema(
        'collect-response',
        Schema(schema_str=json.dumps(models.CollectResponse.schema()), schema_type='JSON'),
    )

    shema_registry_client.register_schema(
        'agent-broadcast-ping',
        Schema(schema_str=json.dumps(models.PingRequest.schema()), schema_type='JSON'),
    )

    shema_registry_client.register_schema(
        'agent-connect',
        Schema(schema_str=json.dumps(models.AgentInfo.schema()), schema_type='JSON'),
    )
    shema_registry_client.register_schema(
        'agent-disconnect',
        Schema(schema_str=json.dumps(models.AgentInfo.schema()), schema_type='JSON'),
    )

    shema_registry_client.register_schema(
        'engine-connect',
        Schema(schema_str=json.dumps(models.EngineInfo.schema()), schema_type='JSON'),
    )

<<<<<<< HEAD
=======
    shema_registry_client.register_schema(
        'scan',
        Schema(schema_str=json.dumps(models.Scan.schema()), schema_type='JSON'),
    )

>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

remove_schemas()
create_schemas()
