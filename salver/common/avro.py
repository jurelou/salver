# -*- coding: utf-8 -*-

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer


def _get_schema(schema_registry_client: SchemaRegistryClient, topic: str) -> str:
    """Return a schema string from an AVRO server."""
    return schema_registry_client.get_latest_version(topic).schema.schema_str


def make_serializer(topic, to_dict, schema_registry_url):
    """Create an AvroSerializer from a topic."""
    client = SchemaRegistryClient({'url': schema_registry_url})
    return AvroSerializer(
        schema_str=_get_schema(client, topic),
        schema_registry_client=client,
        to_dict=to_dict,
    )


def make_deserializer(topic, from_dict, schema_registry_url):
    """Create an AvroDeserializer from a topic."""
    client = SchemaRegistryClient({'url': schema_registry_url})
    return AvroDeserializer(
        schema_str=_get_schema(client, topic),
        schema_registry_client=client,
        from_dict=from_dict,
    )
