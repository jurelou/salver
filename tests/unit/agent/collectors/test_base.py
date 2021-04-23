# -*- coding: utf-8 -*-
from salver.facts import Email, Person
from salver.agent.collectors.base import BaseCollector
from salver.agent import exceptions
import pytest
from salver.common.limiter import Duration, RequestRate
import time
from salver.common.exceptions import BucketFullException


def test_base_collector():

    class TestCollector(BaseCollector):
        config = {
            "name": "base-collector",
            "limiter": [RequestRate(limit=1, interval=Duration.SECOND)],
        }


    with pytest.raises(exceptions.InvalidCollectorDefinition):
        TestCollector()

def test_base_rate_limit():

    class TestCollector(BaseCollector):
        config = {
            "name": "base-collector",

        }

        def callbacks(self):
            return {Person: self.cb}
        
        def cb(self, person):
            return Person(firstname=f"res-{person.firstname}", lastname=f"res-{person.lastname}")


    collector = TestCollector()

    res = collector.collect([
        Person(firstname="test-base-collector-812", lastname="test-base-collector-918"),
        Person(firstname="test-base-collector-719", lastname="test-base-collector-313")
    ])

    print("======", res)

    # try:
    #     collector.check_rate_limit()
    # except BucketFullException as err:
    #     logger.warning(f"Retry scan of {collector_name} in {err.remaining_time}s")
    #     raise self.retry(countdown=err.remaining_time, exc=err)

    # collect_result, facts = collector.collect(facts)