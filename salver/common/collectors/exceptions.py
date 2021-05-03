# -*- coding: utf-8 -*-
from salver.common.exceptions import SalverException


class CollectorException(SalverException):
    """Base collector exceptions."""

    def __init__(self, collector_name):
        self.collector_name = collector_name


class CollectorNotFound(CollectorException):
    def __str__(self):
        return f'Collector {self.collector_name} not found'


# class CollectorDisabled(CollectorException):
#     def __str__(self):
#         return f'Collector {self.collector_name} is disabled'


class InvalidCollectorDefinition(CollectorException):
    def __init__(self, collector_name, error):
        self.collector_name = collector_name
        self.error = error

    def __str__(self):
        return f'Invalid collector definition for {self.collector_name}: {self.error}'


class CollectorRuntimeError(CollectorException):
    def __init__(self, collector_name, error):
        self.collector_name = collector_name
        self.error = error

    def __str__(self):
        return f'Collector runtime error for {self.collector_name}: {self.error}'


class MissingCollectorDefinition(CollectorException):
    def __str__(self):
        return f"Can't find `{self.collector_name}`, which is defined \
        in the configuration file. Check your settings.yml file `collectors` section."
