# -*- coding: utf-8 -*-
from salver.common import limiter
import time
import pytest
from salver.common.exceptions import BucketFullException


def test_limiter_00():
    l = limiter.Limiter(limiter.RequestRate(limit=1, interval=limiter.Duration.SECOND))

    l.try_acquire()
    with pytest.raises(BucketFullException) as err:
        l.try_acquire()
    time.sleep(err.value.remaining_time)
    l.try_acquire()
