# -*- coding: utf-8 -*-
import sys
import json
import time

from confluent_kafka.admin import NewTopic, AdminClient
from confluent_kafka.schema_registry import Schema, SchemaRegistryClient

from salver.common import models
from salver.common.facts import all_facts

topics = [
    'agent-broadcast-ping',
    'engine-connect',
    'agent-disconnect',
    'agent-collect-create',
    # 'agent-collect-item',
    # 'agent-collect-update-status',
]

admin_client = AdminClient({'bootstrap.servers': 'localhost:9092'})
shema_registry_client = SchemaRegistryClient({'url': 'http://127.0.0.1:8081'})


def delete_topics():
    fs = admin_client.delete_topics(topics)
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f'Topic {topic} deleted')
        except Exception as e:
            print('Failed to delete topic {}: {}'.format(topic, e))
    time.sleep(2)  # For some reasons changes are not applied directly ....


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


def resolve_type(pydantic_type):
    if pydantic_type == 'integer':
        return 'int'
    return pydantic_type


def get_facts_avro_mapping():
    for fact in all_facts.values():
        schema = fact.schema()
        fields = [
            {'name': p_name, 'type': resolve_type(p_value['type'])}
            for p_name, p_value in schema['properties'].items()
        ]
        fields.append(
            {'name': '__fact_type__', 'type': 'string', 'default': schema['title']},
        )
        yield {
            'name': schema['title'],
            'type': 'record',
            'fields': fields,
        }


def pydantic_to_avro(pydantic_model):
    """Converts a pydantic model to avro."""

    pydantic_schema = pydantic_model.schema()
    properties = []

    for p_name, p_value in pydantic_schema['properties'].items():
        p_type = p_value['type']
        if p_type == 'array':

            if '$ref' in p_value['items']:
                if 'BaseFact' in p_value['items']['$ref']:
                    items = list(get_facts_avro_mapping())

                else:
                    if '#/definition' not in p_value['items']['$ref']:
                        print(f'ERRORRRRRRR, could not parse field {p_name}: {p_value}')
                        sys.exit(1)

                    a = getattr(
                        models, p_value['items']['$ref'].split('#/definitions/')[1],
                    )
                    model_json = pydantic_to_avro(a)
                    model = json.loads(model_json)
                    items = {
                        'name': model['name'],
                        'type': 'record',
                        'fields': model['fields'],
                    }

            else:
                items = resolve_type(p_value['items']['type'])

            new_p_type = {
                'type': 'array',
                'items': items,
            }

        else:
            new_p_type = resolve_type(p_value['type'])
        properties.append(
            {
                'name': p_name,
                'type': new_p_type,
            },
        )

    title = pydantic_schema['title']
    return json.dumps(
        {
            'namespace': f'salver.{title}',
            'name': title,
            'type': 'record',
            'fields': properties,
        },
    )


def remove_schemas():
    for subject in shema_registry_client.get_subjects():
        print('Remobe schema subject', subject)
        shema_registry_client.delete_subject(subject)


def create_schemas():
    collect_request = Schema(
        schema_str=pydantic_to_avro(models.Collect),
        schema_type='AVRO',
    )

    ping_request = Schema(
        schema_str=pydantic_to_avro(models.PingRequest),
        schema_type='AVRO',
    )

    engine_info = Schema(
        schema_str=pydantic_to_avro(models.EngineInfo),
        schema_type='AVRO',
    )

    agent_info = Schema(
        schema_str=pydantic_to_avro(models.AgentInfo),
        schema_type='AVRO',
    )

    shema_registry_client.register_schema('agent-broadcast-ping', ping_request)
    shema_registry_client.register_schema('agent-collect-create', collect_request)

    shema_registry_client.register_schema('agent-connect', agent_info)
    shema_registry_client.register_schema('agent-disconnect', agent_info)

    shema_registry_client.register_schema('engine-connect', engine_info)

    # shema_registry_client.register_schema('request-agent-info', info_request)
    # shema_registry_client.register_schema('agent-info', info_response)


remove_schemas()
create_schemas()
