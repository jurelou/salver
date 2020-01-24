from abc import ABC, abstractmethod


class TimeLimit(ABC):

    @abstractmethod
    def __init__(self, tokens, timevalue=1):
        pass

    @abstractmethod
    def getTime(self):
        pass
