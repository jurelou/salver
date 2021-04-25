from pydantic import BaseModel
from typing import Dict, Optional
from salver.common.kafka import Producer, Consumer, ConsumerAPI


class   Topic:
    def __init__(self,
        name: str,
        model_serializer: BaseModel,
        schema_registry_url: str,
        kafka_config: Dict[str, str],
        consumer_threads: int, consumer_workers: int, consumer_api: Optional[ConsumerAPI] = None, consume: bool = False, produce: bool =False):

        self.consumer = None
        self.producer = None

        #maybe split kafka_config to consumer_config && producer_config and common kafka_config
        #verify fields, if fiels exists when consume=True, ...
        if self.produce:
            self.producer = Producer(
                topic=topic,
                value_serializer=model_serializer.to_dict,
                schema_registry_url=schema_registry_url,
                kafka_config=kafka_config
            )
            
        if self.consume:
            self.consumer = Consumer(
                topic=topic,
                num_workers=consumer_workers,
                num_threads=consumer_threads,
                value_deserializer=model_serializer.from_dict,
                schema_registry_url=schema_registry_url,
                kafka_config=kafka_config,
                callback_cls=consumer_api
            )