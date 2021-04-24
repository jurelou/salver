from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
import json


# TODO: cache schema registry client
def _get_schema(schema_registry_client, topic) -> str:
        return schema_registry_client.get_latest_version(topic).schema.schema_str

def make_serializer(topic, to_dict, schema_registry_url):
        client = SchemaRegistryClient({'url': schema_registry_url})
        return AvroSerializer(
                schema_str=_get_schema(client, f"{topic}-value"),
                schema_registry_client=client,
                to_dict=to_dict)


def make_deserializer(topic, from_dict, schema_registry_url):
        client = SchemaRegistryClient({'url': schema_registry_url})
        return AvroDeserializer(
                schema_str=_get_schema(client, f"{topic}-value"),
                schema_registry_client=client,
                from_dict=from_dict)
