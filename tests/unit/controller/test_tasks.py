# -*- coding: utf-8 -*-
from salver.controller import tasks, exceptions
from mock import patch
import pytest
from tests import api
from tests import datasets

def test_reload_agents():
    tasks.reload_agents.apply().get()
    agents = tasks.list_agents.apply().get()
    assert len(agents) == 1

def test_ping():
    ping = tasks.ping.apply()
    assert ping.get() == 'pong'

def test_scan():
    # tasks.reload_agents.apply().get()

    t = tasks.launch_scan.s(datasets.UNIT_CONTROLLER_SCAN_1).apply_async()
    res = t.get_leaf()



"""
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
"""
