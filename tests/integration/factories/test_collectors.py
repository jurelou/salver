# -*- coding: utf-8 -*-
from mock import patch
from salver.agent.collectors.factory import CollectorFactory
import pytest
from salver.agent import exceptions
from salver.agent.collectors.docker import DockerCollector
from salver.agent.collectors.base import BaseCollector

class DummyDocker(DockerCollector):
    config = { 'name': 'dummy-docker', 'docker': {'image': 'alpine'}}

    def callbacks(self):
        return {}

class DummyDockerBis(DockerCollector):
    config = { 'name': 'dummy-docker', 'docker': {'image': 'another'}}

    def callbacks(self):
        return {}

class Dummy(BaseCollector):
    config = {'name': 'dummy'}

    def callbacks(self):
        return {}

class ErroredDocker(DockerCollector):
    def callbacks(self):
        return {}

class ErroredDocker2(DockerCollector):
    config = { 'docker': {'image': 'alpine'}}

    def callbacks(self):
        return {}

@patch('salver.agent.collectors.factory.ENABLED_COLLECTORS', ['collector-xxxxxxx'])
def test_factory_1():
    with pytest.raises(exceptions.MissingCollectorDefinition):
        factory = CollectorFactory().build()


@patch('salver.agent.collectors.factory.ENABLED_COLLECTORS', ['dummy-docker', 'dummy', 'collector-c'])
@patch('salver.agent.collectors.factory.CollectorFactory.load_classes_from_module')
def test_factory_2(mock_load):
    mock_load.return_value = [Dummy, DummyDocker]
    with pytest.raises(exceptions.MissingCollectorDefinition):
        factory = CollectorFactory().build()

@patch('salver.agent.collectors.factory.ENABLED_COLLECTORS', ['dummy-docker', 'dummy'])
@patch('salver.agent.collectors.factory.CollectorFactory.load_classes_from_module')
def test_factory_3(mock_load):
    mock_load.return_value = [Dummy, DummyDocker]
    collectors = CollectorFactory().build()
    assert len(collectors.keys()) == 2

    assert collectors['dummy']['active'] == True
    assert isinstance(collectors['dummy']['instance'], Dummy)

    assert collectors['dummy-docker']['active'] == True
    assert isinstance(collectors['dummy-docker']['instance'], DummyDocker)


@patch('salver.agent.collectors.factory.ENABLED_COLLECTORS', ['dummy-docker'])
@patch('salver.agent.collectors.factory.CollectorFactory.load_classes_from_module')
def test_factory_errored_4(mock_test):
    mock_test.return_value = [DummyDocker, Dummy]
    collectors = CollectorFactory().build()

    assert len(collectors.keys()) == 2

    assert collectors['dummy'] == {'active': False, 'instance': None}

    assert isinstance(collectors['dummy-docker']['instance'], DummyDocker)
    assert collectors['dummy-docker']['active'] == True


@patch('salver.agent.collectors.factory.ENABLED_COLLECTORS', ['errored-docker'])
@patch('salver.agent.collectors.factory.CollectorFactory.load_classes_from_module')
def test_factory_errored_1(mock_test):
    mock_test.return_value = [ErroredDocker]
    with pytest.raises(exceptions.InvalidCollectorDefinition):
        collectors = CollectorFactory().build()

@patch('salver.agent.collectors.factory.ENABLED_COLLECTORS', ['errored-docker2'])
@patch('salver.agent.collectors.factory.CollectorFactory.load_classes_from_module')
def test_factory_errored_2(mock_test):
    mock_test.return_value = [ErroredDocker2]
    with pytest.raises(exceptions.InvalidCollectorDefinition):
        collectors = CollectorFactory().build()
