# -*- coding: utf-8 -*-
from opulence.common.exceptions import OpulenceException


class EngineException(OpulenceException):
    """Base engine exceptions."""


# class CollectorException(AgentException):
#     def __init__(self, collector_name):
#         self.collector_name = collector_name



# class CollectorNotFound(CollectorException):
#     def __str__(self):
#         return f"Collector {self.collector_name} not found"
