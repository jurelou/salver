# -*- coding: utf-8 -*-

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer, JSONDeserializer


def _get_schema(schema_registry_client: SchemaRegistryClient, topic: str) -> str:
    """Return a schema string from an AVRO server."""
    return schema_registry_client.get_latest_version(topic).schema.schema_str


def make_serializer(subject, to_dict, schema_registry_url):
    """Create an AvroSerializer from a topic."""
    client = SchemaRegistryClient({'url': schema_registry_url})
    return JSONSerializer(
        schema_str=_get_schema(client, subject),
        schema_registry_client=client,
        to_dict=to_dict,
        conf={'auto.register.schemas': True},
    )


def make_deserializer(subject, from_dict, schema_registry_url):
    """Create an AvroDeserializer from a topic."""
    client = SchemaRegistryClient({'url': schema_registry_url})
    return JSONDeserializer(
        schema_str=_get_schema(client, subject),
        from_dict=from_dict,
    )
