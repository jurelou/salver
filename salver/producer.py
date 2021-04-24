import argparse
from uuid import uuid4

from six.moves import input

from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import time

from schema import *


# def delivery_report(err, msg):
#     if err is not None:
#         print("Delivery failed for User record {}: {}".format(msg.key(), err))
#         return
#     print('User record {} successfully produced to {} [{}] at offset {}'.format(
#         msg.key(), msg.topic(), msg.partition(), msg.offset()))

# def produce_loop(producer):
#     topic = "topic2"
#     print("Producing user records to topic {}. ^C to exit.".format(topic))

#     while True:
#         # Serve on_delivery callbacks from previous calls to produce()
#         try:
#             user_name = input("Enter name: ")
#             user_favorite_color = input("Enter favorite color: ")
#             user = User(name=user_name,
#                         favorite_color=user_favorite_color)
#             print("PROD")
#             producer.poll(0.0)
#             producer.produce(topic=topic, key=str(uuid4()), value=user,
#                              on_delivery=delivery_report)

#             # producer.produce(topic=topic, key=str(uuid4()), value="salut",
#             #                  on_delivery=delivery_report)

#         except KeyboardInterrupt:
#             break
#         except ValueError:
#             print("Invalid input, discarding record...")
#             continue

#     print("\nFlushing records...")
#     producer.flush()

# def main():
#     sr_conf = {'url': "http://127.0.0.1:8081"}
#     schema_registry_client = SchemaRegistryClient(sr_conf)
#     avro_serializer = AvroSerializer(schema_str=schema_str, schema_registry_client=schema_registry_client, to_dict=user_to_dict)
#     string_serializer = StringSerializer('utf_8')

#     producer_conf = {'bootstrap.servers': 'localhost:9092',
#                      'key.serializer': string_serializer,
#                      'value.serializer': avro_serializer}

#     producer = SerializingProducer(producer_conf)


#     produce_loop(producer)

class   Producer:
    def __init__(self, config, topic):
        self.producer = SerializingProducer(config)
        self.topic = topic

    @staticmethod
    def _delivery_report(err, msg):
        if err is not None:
            print("Delivery failed for User record {}: {}".format(msg.key(), err))
            return
        print('User record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()))


    def produce(self, msg, flush=False):
        print(f"Producing ecords to topic {self.topic}: {msg}")

        self.producer.poll(0.0)
        self.producer.produce(topic=self.topic, key=str(uuid4()), value=msg,
                        on_delivery=self._delivery_report)
        if flush:
            self.flush()

    def flush(self):
        self.producer.flush()

class   EngineProducer:
    def __init__(self):
        sr_conf = {'url': "http://127.0.0.1:8081"}
        schema_registry_client = SchemaRegistryClient(sr_conf)
        avro_serializer = AvroSerializer(schema_str=schema_str, schema_registry_client=schema_registry_client, to_dict=user_to_dict)
        string_serializer = StringSerializer('utf_8')

        producer_conf = {'bootstrap.servers': 'localhost:9092',
                        'key.serializer': string_serializer,
                        'value.serializer': avro_serializer}


        self.scan_producer = Producer(
                config=producer_conf,
                topic="topic1"
            )

        self.topic2_producer = Producer(
                config=producer_conf,
                topic="topic2"
            )

    def go(self):
        user = User(name="uname111",
                    listof=["a11", "b11", "c111"],
                    favorite_color="favcol111")
    
        user2 = User(name="uname222",
                    listof=["a", "b", "c"],
                    favorite_color="favcol222")

        while True:
            self.scan_producer.produce(user)
            self.topic2_producer.produce(user2)

            time.sleep(5)

e = EngineProducer()
e.go()

# main()