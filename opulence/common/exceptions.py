# -*- coding: utf-8 -*-
class BaseOpulenceException(Exception):
    pass


class TaskTimeoutError(BaseOpulenceException):
    def __init__(self, value=None):
        self.value = value or ""

    def __str__(self):
        return f"Celery task timeout: ({self.value})"


class CollectorNotFound(BaseOpulenceException):
    def __init__(self, collector_name):
        self.collector_name = collector_name

    def __str__(self):
        return f"Collector {self.collector_name} not found"

class BucketFullException(BaseOpulenceException):
    def __init__(self, rate, remaining_time):
        self.remaining_time = remaining_time
        self.rate = rate
        super().__init__(f"Bucket with Rate {rate} is full")