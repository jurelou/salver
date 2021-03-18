# -*- coding: utf-8 -*-
from abc import ABC
from abc import abstractmethod


class TimeLimit(ABC):
    @abstractmethod
    def __init__(self, tokens, timevalue=1):
        pass

    @abstractmethod
    def getTime(self):
        pass
