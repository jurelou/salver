
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

from salver.common import models
from salver.config import agent_config
from salver.common.kafka import Producer
from salver.agent.services.kafka_producers import KafkaProducers
from salver.agent.services.kafka_consumers import KafkaConsumers


class ConsumerAPI:
    def __init__(self):
        # self.producers = KafkaProducers()
        self._methods = {
            "agent-collect": self.on_collect,
            "agent-info": self.on_info_request,
            "agent-broadcast-ping": self.on_ping

        }
    def get_method_for_topic(self, topic: str):
        if topic in self._methods:
            return self._methods[topic]
        return None  

    def on_info_request(self, info_request):
        print("INFO REQUEST", info_request)
        # self.producers.info_response.produce(models.AgentInfo(name="yesssssssss"), flush=True)

    def on_collect(self, toto):
        print("COLLECt", toto)
    
    def on_ping(self, ping):
        print("PINGPING", ping)
        # self.producers.info_response.produce(models.AgentInfo(name="yesssssssss"))
        # self.producers.info_response.flush()

class AgentAPI:
    # producers = {

    #     "agent-info-response": Producer(
    #         topic='agent-info-response',
    #         value_serializer=models.AgentInfo.to_dict,
    #         schema_registry_url=agent_config.kafka.schema_registry_url,
    #         kafka_config={
    #             'bootstrap.servers': agent_config.kafka.bootstrap_servers,
    #         },
    #     )


    def __init__(self):
        print("CREATE AGENT API")

        self.consumers = KafkaConsumers(ConsumerAPI)
    def start(self):
        self.consumers.start()