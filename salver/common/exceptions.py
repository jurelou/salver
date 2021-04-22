# -*- coding: utf-8 -*-
class OpulenceException(Exception):
    """Raise a base opulence exception."""


# class TaskTimeoutError(BaseOpulenceException):
#     def __init__(self, value=None):
#         self.value = value or ""

#     def __str__(self):
#         return f"Celery task timeout: ({self.value})"


class BucketFullException(OpulenceException):
    def __init__(self, rate, remaining_time):
        self.remaining_time = remaining_time
        self.rate = rate

    def __str__(self):
        return f'Bucket with Rate {self.rate.limit}/{self.rate.interval.name} is full'
