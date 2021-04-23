# -*- coding: utf-8 -*-
from salver.facts import Email, Person
from salver.common.utils import get_actual_dir
from salver.agent.collectors.docker import DockerCollector
from salver.agent import exceptions
import pytest


def test_invalid_docker_1():

    class SomeDocker(DockerCollector):
        config = {
            "name": "dummy-docker-collector",
        }

        def callbacks(self):
            return {}

    with pytest.raises(exceptions.InvalidCollectorDefinition):
        docker_collector = SomeDocker()

def test_invalid_docker_2():

    class SomeDocker(DockerCollector):
        config = {
            "name": "dummy-docker-collector",
            "docker": {"image": "some image", "build_context": "some context"},
        }

        def callbacks(self):
            return {}

    with pytest.raises(exceptions.InvalidCollectorDefinition):
        docker_collector = SomeDocker()

def test_invalid_docker_3():

    class SomeDocker(DockerCollector):
        config = {
            "name": "dummy-docker-collector",
            "docker": {"build_context": "/tmp/this/should/not/exists"},
        }

        def callbacks(self):
            return {}

    with pytest.raises(exceptions.InvalidCollectorDefinition):
        docker_collector = SomeDocker()

def test_invalid_docker_4():

    class SomeDocker(DockerCollector):
        config = {
            "name": "dummy-docker-collector",
            "docker": {"image": "this_docker_image_does_not_exists"},
        }

        def callbacks(self):
            return {}

    with pytest.raises(exceptions.InvalidCollectorDefinition):
        docker_collector = SomeDocker()