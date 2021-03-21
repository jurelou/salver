from opulence.common import limiter
from mock import patch
import time
import itertools
import pytest
from opulence.common.exceptions import BucketFullException

# def frange(start, end, step):
#     assert (step != 0)
#     sample_count = int(abs(end - start) / step)
#     return itertools.islice(itertools.count(start, step), sample_count)

def test_limiter_00():
    l = limiter.Limiter(limiter.RequestRate(limit=1, interval=limiter.Duration.SECOND))

    l.try_acquire()
    with pytest.raises(BucketFullException) as err:
        l.try_acquire()
    time.sleep(err.value.remaining_time)
    l.try_acquire()
