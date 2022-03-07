# -*- coding: utf-8 -*-
import time
from enum import IntEnum
from queue import Queue
from typing import Tuple

from loguru import logger
from pydantic import BaseModel

from salver.common.exceptions import RateLimitException

class Duration(IntEnum):
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 3600 * 24
    MONTH = 3600 * 24 * 30


class RequestRate(BaseModel):
    limit: int
    interval: Duration


class Bucket:
    """A bucket that resides in memory using python's built-in Queue."""

    def __init__(self, maxsize=0):
        self._q = Queue(maxsize=maxsize)

    def inspect_expired_items(self, start_time: int) -> Tuple[int, int]:
        """Find how many items in bucket that have slipped out of the time-window."""
        volume = self.size()
        for log_idx, log_item in enumerate(list(self._q.queue)):
            if log_item > start_time:
                return volume - log_idx, log_item - start_time
        return 0, 0

    def size(self):
        return self._q.qsize()

    def put(self, item):
        self._q.put(item)

    def get(self, number):
        counter = 0
        for _ in range(number):
            self._q.get()
            counter += 1
        return counter


class Limiter:
    """Basic rate-limiter class that makes use of built-in python Queue."""

    def __init__(
        self,
        name,
        *rates: RequestRate,
    ):
        self._validate_rate_list(rates)
        self._rates = rates
        self._name = name
        self._bucket: Bucket = Bucket(maxsize=self._rates[-1].limit)

    @staticmethod
    def _validate_rate_list(rates):
        if not rates:
            raise ValueError("Rate(s) must be provided")

        for idx, rate in enumerate(rates[1:]):
            prev_rate = rates[idx]
            invalid = (
                rate.limit <= prev_rate.limit
                or rate.interval.value <= prev_rate.interval.value
            )
            if invalid:
                raise ValueError(f"{prev_rate} cannot come before {rate}")

    def try_acquire(self) -> None:
        """Acquiring an item or reject it if rate-limit has been exceeded."""

        now = int(time.time())
        for idx, rate in enumerate(self._rates):
            if self._bucket.size() < rate.limit:
                continue

            start_time = now - rate.interval.value
            item_count, remaining_time = self._bucket.inspect_expired_items(start_time)
            if item_count >= rate.limit:
                raise RateLimitException(rate, remaining_time)
            if idx == len(self._rates) - 1:
                self._bucket.get(self._bucket.size() - item_count)
        self._bucket.put(now)

    def rate_limit(self) -> None:
        """Acquire an item or sleep untill an item in available."""
        try:
            self.try_acquire()
        except RateLimitException as err:
            logger.info(
                f"Rate limit reached for {self._name}, sleeping for {err.remaining_time}s",
            )
            time.sleep(err.remaining_time)
