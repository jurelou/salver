# -*- coding: utf-8 -*-
from mock import patch
import pytest
from salver.agent import tasks
from salver.common import exceptions

import uuid

from salver.common.facts import Person, Email

@patch('salver.agent.tasks.current_task')
def test_dummy_docker_collector(mock_current_task):
    mock_current_task.request.delivery_info = {'routing_key': 'dummy-collector'}
    res = tasks.scan.s(
        uuid.uuid4(),
        [
            Person(firstname='agent-test', lastname='dummy-collector'),
            Email(address='agenttest@dummydocker.collector'),
        ],
    ).apply()
    result = res.get()
    # print("!!!", result)
    # assert result['duration'] < 5
    # assert result['executions_count'] == 2
    # assert len(result['facts']) == 4
