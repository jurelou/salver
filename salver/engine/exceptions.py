# -*- coding: utf-8 -*-
from salver.common.exceptions import SalverException

class CollectorNotFound(SalverException):
    def __init__(self, collector_name):
        self.collector_name = collector_name

    def __str__(self):
        return f'Collector {self.collector_name} not found.'