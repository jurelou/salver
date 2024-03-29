# -*- coding: utf-8 -*-
from salver.common.facts import Email, Person
from salver.agent.collectors import BaseCollector

from salver.common import exceptions
import pytest
from salver.common.limiter import Duration, RequestRate
import time
from uuid import uuid4

def test_base_collector():

    class TestCollector(BaseCollector):
        config = {
            'name': 'base-collector',
        }

    with pytest.raises(exceptions.InvalidCollectorDefinition) as err:
        TestCollector()

def test_base_rate_limit():

    class TestCollector(BaseCollector):
        config = {
            'name': 'base-collector',
            'limiter': [RequestRate(limit=1, interval=Duration.SECOND)],
        }

        def callbacks(self):
            return {Person: self.cb}

        def cb(self, person):
            print("!!!!")
            return Person(firstname=f'res-{person.firstname}', lastname=f'res-{person.lastname}')


    collector = TestCollector()

    collector.collect(collect_id=uuid4(), facts=[Person(firstname='42', lastname='42')])
    collector.collect(collect_id=uuid4(), facts=[Person(firstname='42', lastname='42')])
    collector.collect(collect_id=uuid4(), facts=[Person(firstname='42', lastname='42')])
    
    return

    with pytest.raises(exceptions.RateLimitException) as err:
        collector.collect(collect_id=uuid4(), facts=[Person(firstname='42', lastname='42')])
    time.sleep(err.value.remaining_time)
    collector.collect(collect_id=uuid4(), facts=[Person(firstname='42', lastname='42')])

# def test_output_1():
#     class TestCollector(BaseCollector):
#         config = {
#             'name': 'base-collector',
#         }

#         def callbacks(self):
#             return {Person: self.cb}

#         def cb(self, person):
#             yield None
#             yield [Person(firstname='a', lastname='b'), Email(address='c')]
#             yield Person(firstname='d', lastname='d')
#             yield None
#             yield 'nope'
#             yield 42
#             yield []
#             yield (1, 3)

#     collector = TestCollector()
#     result, facts = collector.collect([Person(firstname='test-base-collector', lastname='test-base-collector')])
#     assert result.executions_count == 1
#     assert len(result.facts) == 3
#     assert len(facts) == 3


# def test_output_2():
#     class TestCollector(BaseCollector):
#         config = {
#             'name': 'base-collector',
#         }

#         def callbacks(self):
#             return {Person: self.cb}

#         def cb(self, person):
#             return [Person(firstname='a', lastname='b'), Email(address='c')]

#     collector = TestCollector()
#     result, facts = collector.collect([Person(firstname='test-base-collector', lastname='test-base-collector')])
#     assert result.executions_count == 1
#     assert len(result.facts) == 2
#     assert len(facts) == 2

# def test_output_3():
#     class TestCollector(BaseCollector):
#         config = {
#             'name': 'base-collector',
#         }

#         def callbacks(self):
#             return {Person: self.cb}

#         def cb(self, person):
#             pass
#     collector = TestCollector()
#     result, facts = collector.collect([Person(firstname='test-base-collector', lastname='test-base-collector')])
#     assert result.executions_count == 1
#     assert len(result.facts) == 0
#     assert facts == []

# def test_output_4():
#     class TestCollector(BaseCollector):
#         config = {
#             'name': 'base-collector',
#         }

#         def callbacks(self):
#             return {Person: self.cb}

#         def cb(self, person):
#             return 'nope'

#     collector = TestCollector()
#     result, facts = collector.collect([Person(firstname='test-base-collector', lastname='test-base-collector')])
#     assert result.executions_count == 1
#     assert len(result.facts) == 0
#     assert len(facts) == 0

# def test_output_raises():
#     class TestCollector(BaseCollector):
#         config = {
#             'name': 'base-collector',
#         }

#         def callbacks(self):
#             return {Person: self.cb}

#         def cb(self, person):
#             raise ValueError('aze')

#     collector = TestCollector()
#     with pytest.raises(exceptions.CollectorRuntimeError):
#         collector.collect([Person(firstname='test-base-collector', lastname='test-base-collector')])
