#!/bin/bash

docker exec mongo1 /usr/bin/mongo --eval '''if (rs.status()["ok"] == 0) {
    rsconf = {
      _id : "rs0",
      members: [
        { _id : 0, host : "mongo1:27017", priority: 1.0 },
        { _id : 1, host : "mongo2:27017", priority: 0.5 },
        { _id : 2, host : "mongo3:27017", priority: 0.5 }
      ]
    };
    rs.initiate(rsconf);
}
rs.conf();'''

# curl -X POST -H "Content-Type: application/json" --data '
#   { "name": "datagen-agent-connect",
#     "config": {
#       "connector.class": "io.confluent.kafka.connect.datagen.DatagenConnector",
#       "kafka.topic": "agent-connect",
#       "quickstart": "agent-connect",
#       "key.converter": "org.apache.kafka.connect.json.JsonConverter",
#       "value.converter": "org.apache.kafka.connect.json.JsonConverter",
#       "value.converter.schemas.enable": "false",
#       "producer.interceptor.classes": "io.confluent.monitoring.clients.interceptor.MonitoringProducerInterceptor",
#       "max.interval": 200,
#       "iterations": 10000000,
#       "tasks.max": "1"
# }}' http://localhost:8083/connectors -w "\n"

curl -X POST -H "Content-Type: application/json" --data '
  {"name": "mongo-sink-agent-connect",
   "config": {
     "connector.class":"com.mongodb.kafka.connect.MongoSinkConnector",
     "tasks.max":"1",
     "topics":"agent-connect",
     "connection.uri":"mongodb://mongo1:27017,mongo2:27017,mongo3:27017",
     "database":"salver",
     "collection":"agents",
     "key.converter": "org.apache.kafka.connect.storage.StringConverter",

     "value.converter": "io.confluent.connect.avro.AvroConverter",
     "value.converter.schema.registry.url": "http://schema-registry:8081",
     "value.converter.schemas.enable": "true"
}}' http://localhost:8083/connectors -w "\n"
