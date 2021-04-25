from typing import Callable, Dict

class ConsumerAPI:
    def __init__(self, topic):
        self.topic = topic
        
        # if not self.methods:
        #     raise ValueError(f"ConsumerAPI {type(self)} should have a `methods` property")
        # print(f"Create ConsumerAPI {type(self)}")

    # @property
    # def methods(self) -> Dict[str, Callable]:
    #     return {}

    # def get_method_for_topic(self, topic: str) -> Callable:
    #     raise NotImplementedError(f"ConsumerAPI {type(self)} does not implements `get_method_for_topic`")
