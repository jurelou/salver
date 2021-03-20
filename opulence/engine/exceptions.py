# -*- coding: utf-8 -*-
from opulence.common.exceptions import OpulenceException


class EngineException(OpulenceException):
    """Base engine exceptions."""


class CollectorNotFound(EngineException):
    def __init__(self, collector_name):
        self.collector_name = collector_name

    def __str__(self):
        return f"Collector {self.collector_name} not found"

# class CollectorNotFound(CollectorException):
#     def __str__(self):
#         return f"Collector {self.collector_name} not found"