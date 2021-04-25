from salver.common import models
from salver.engine.services.kafka_producers import KafkaProducers
from salver.engine.services.kafka_consumers import KafkaConsumers

from salver.common.kafka import ConsumerAPI, Topic
from salver.config import engine_config


from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager


class ConsumeAPI():

    def __init__(self):
        self._methods = {
            "agent-info-response": self.on_info_response,
            "agent-broadcast-ping": self.on_ping
        }

        self.producers = KafkaProducers()

    def on_ping(self, msg):
        print("ON PING", msg)
        # self.producers.agents_broadcast.produce(models.PingRequest(), flush=True)

    def on_info_response(self, toto):
        print("INFO RESPONSE", toto)
        self.producers.agents_broadcast.produce(models.PingRequest(ping="world"), flush=True)
        # self.producers.agents_broadcast.produce(models.PingRequest(ping="world"), flush=True)
        # self.producers.agents_broadcast.produce(models.PingRequest(ping="world"), flush=True)

    def get_method_for_topic(self, topic: str):
        if topic in self._methods:
            return self._methods[topic]
        return None    


class EngineAPI:
    def __init__(self, producers = None):
        print("CREATE ENGINE API")

        self.consumers = KafkaConsumers(ConsumeAPI)
        self.consumers.start()
        # toto = Topic(
        #         produce=True,
        #         topic='agent-info-response',
        #         consumer_workers=engine_config.kafka.workers_per_topic,
        #         consumer_threads=engine_config.kafka.threads_per_worker,
        #         model_serializer=models.AgentInfo,
        #         schema_registry_url=engine_config.kafka.schema_registry_url,
        #         kafka_config={
        #             'bootstrap.servers': engine_config.kafka.bootstrap_servers,
        #             'group.id': 'engine',
        #         },
        #         callback_cls=callback_cls
        #     ),
        # self.producers = KafkaProducers()
        


