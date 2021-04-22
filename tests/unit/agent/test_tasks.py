# -*- coding: utf-8 -*-
from salver.agent import tasks, exceptions
from mock import patch
from salver.facts import Person, Email
import pytest


def test_ping():
    ping = tasks.ping.apply()
    assert ping.get() == 'pong'


@patch('salver.agent.tasks.current_task')
def test_invalid_collector(mock_current_task):
    mock_current_task.request.delivery_info = {
        'routing_key': 'thiscollectorwillneverexists',
    }
    res = tasks.scan.s([]).apply()

    with pytest.raises(exceptions.CollectorNotFound):
        res.get()


@patch('salver.agent.tasks.current_task')
def test_dummy_docker_collector(mock_current_task):
    mock_current_task.request.delivery_info = {'routing_key': 'dummy-docker-collector'}
    res = tasks.scan.s(
        [
            Person(firstname='agent-test', lastname='dummy-docker-collector'),
            Email(address='agenttest@dummydocker.collector'),
        ],
    ).apply()
    result = res.get()

    assert result['duration'] < 5
    assert result['executions_count'] == 2
    assert len(result['facts']) == 4
