# -*- coding: utf-8 -*-
class SalverException(Exception):
    """Base Salver exceptions class."""


class RateLimitException(SalverException):
    def __init__(self, rate, remaining_time):
        self.remaining_time = remaining_time
        self.rate = rate

    def __str__(self):
        return f'Bucket with Rate {self.rate.limit}/{self.rate.interval.name} is full'
