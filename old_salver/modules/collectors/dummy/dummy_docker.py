# -*- coding: utf-8 -*-
from salver.facts import Email, Person
from salver.common.utils import get_actual_dir
from salver.agent.collectors.docker import DockerCollector


class DummyDocker(DockerCollector):
    config = {
        'name': 'dummy-docker-collector',
        'docker': {'build_context': get_actual_dir()},
    }

    def callbacks(self):
        return {
            Person: self.cb_person,
            Email: self.cb_email,
        }

    def cb_person(self, person):
        whoami = self.run_container(command='whoami')
        yield Person(firstname='dummy docker', lastname=whoami)
        yield Email(address='dummy@email')

    def cb_email(self, email):
        date = self.run_container(command='date')
        yield Person(firstname='dummy docker', lastname=date)
        yield Email(address='dummy@email')
