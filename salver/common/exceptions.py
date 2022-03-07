# -*- coding: utf-8 -*-
class SalverException(Exception):
    """Base Salver exceptions class."""


class RateLimitException(SalverException):
    def __init__(self, rate, remaining_time):
        self.remaining_time = remaining_time
        self.rate = rate

    def __str__(self):
        return f"Bucket with Rate {self.rate.limit}/{self.rate.interval.name} is full"


###############################################################
# Collector exceptions
###############################################################
class BaseCollectorException(SalverException):
    def __init__(self, collector_name: str, error: str = ""):
        self.collector_name = collector_name
        self.error = error


class InvalidCollectorDefinition(BaseCollectorException):
    def __str__(self):
        return f"Invalid definition for collector {self.collector_name}: {self.error}"


class CollectorRuntimeError(BaseCollectorException):
    def __str__(self):
        return f"Collector runtime error for {self.collector_name}: {self.error}"


class collectorNotFound(BaseCollectorException):
    def __str__(self):
        return f"Collector {self.collector_name} not found"
