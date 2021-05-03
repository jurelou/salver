# -*- coding: utf-8 -*-
import httpx

schema_registry_url = 'http://schema-registry:8081'
kafka_connect_url = 'http://localhost:8083'
mongo_url = 'mongodb://mongo1:27017'
mongo_db_name = 'salver'


def create_mongo_sink(topic, collection):
    data = {
        'name': f'mongo-sink-{topic}',
        'config': {
            'connector.class': 'com.mongodb.kafka.connect.MongoSinkConnector',
            'tasks.max': 1,
            'topics': topic,
            'connection.uri': mongo_url,
            'database': mongo_db_name,
            'collection': collection,
            'key.converter': 'org.apache.kafka.connect.storage.StringConverter',
            'value.converter': 'io.confluent.connect.json.JsonSchemaConverter',
            'value.converter.schema.registry.url': schema_registry_url,
            'value.converter.schemas.enable': True,
            'errors.tolerance': 'all',
            'errors.log.enable': 'true',
            'errors.log.include.messages': 'true',
            'errors.deadletterqueue.topic.name': f'dlq.mongo.{mongo_db_name}.{collection}',
            'errors.deadletterqueue.context.headers.enable': 'true',
            'errors.deadletterqueue.topic.replication.factor': 1,
        },
    }
    httpx.delete(f'{kafka_connect_url}/connectors/mongo-sink-{topic}')
    res = httpx.post(f'{kafka_connect_url}/connectors', json=data)
    print(res.json())
    res.raise_for_status()


# create_mongo_sink(topic="agent-connect", collection="agents")
create_mongo_sink(topic='agent-collect-create', collection='collects')


# docker exec mongo1 /usr/bin/mongo --eval '''if (rs.status()["ok"] == 0) {
#     rsconf = {
#       _id : "rs0",
#       members: [
#         { _id : 0, host : "mongo1:27017", priority: 1.0 },
#         { _id : 1, host : "mongo2:27017", priority: 0.5 },
#         { _id : 2, host : "mongo3:27017", priority: 0.5 }
#       ]
#     };
#     rs.initiate(rsconf);
# }
# rs.conf();'''


# curl -X POST -H "Content-Type: application/json" --data '
#   {"name": "mongo-sink-agent-connect",
#    "config": {
#      "connector.class":"com.mongodb.kafka.connect.MongoSinkConnector",
#      "tasks.max":"1",
#      "topics":"agent-connect",
#      "connection.uri":"mongodb://mongo1:27017",
#      "database":"salver",
#      "collection":"agents",
#      "key.converter": "org.apache.kafka.connect.storage.StringConverter",

#      "value.converter": "io.confluent.connect.avro.AvroConverter",
#      "value.converter.schema.registry.url": "http://schema-registry:8081",
#      "value.converter.schemas.enable": "true",

#      "errors.tolerance": "all",
#      "errors.log.enable": "true",
#      "errors.log.include.messages": "true",
#      "errors.deadletterqueue.topic.name": "salver.mongo.dlq",
#      "errors.deadletterqueue.context.headers.enable": "true",
#      "errors.deadletterqueue.topic.replication.factor": 1


# }}' http://localhost:8083/connectors -w "\n"


# curl -X POST -H "Content-Type: application/json" --data '
#   {"name": "mongo-sink-agent-connect",
#    "config": {
#      "connector.class":"com.mongodb.kafka.connect.MongoSinkConnector",
#      "tasks.max":"1",
#      "topics":"agent-connect",
#      "connection.uri":"mongodb://mongo1:27017",
#      "database":"salver",
#      "collection":"agents",
#      "key.converter": "org.apache.kafka.connect.storage.StringConverter",

#      "value.converter": "io.confluent.connect.avro.AvroConverter",
#      "value.converter.schema.registry.url": "http://schema-registry:8081",
#      "value.converter.schemas.enable": "true",

#      "errors.tolerance": "all",
#      "errors.log.enable": "true",
#      "errors.log.include.messages": "true",
#      "errors.deadletterqueue.topic.name": "salver.mongo.dlq",
#      "errors.deadletterqueue.context.headers.enable": "true",
#      "errors.deadletterqueue.topic.replication.factor": 1


# }}' http://localhost:8083/connectors -w "\n"
