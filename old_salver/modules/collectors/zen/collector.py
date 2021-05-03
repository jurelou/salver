# -*- coding: utf-8 -*-
from salver.facts import Email, Tweet, Company, Username
from salver.common.utils import get_actual_dir
from salver.agent.collectors.docker import DockerCollector


class Zen(DockerCollector):
    config = {
        'name': 'zen',
        'docker': {'build_context': get_actual_dir()},
    }

    def callbacks(self):
        return {
            Username: self.from_username,
            Company: self.from_company,
        }

    def from_username(self, username):
        data = self.run_container(command=[username.name])
        for email in self.findall_regex(data, fr'{username.name} : (.*)'):
            yield Email(address=email)

    def from_company(self, company):
        data = self.run_container(command=[company.name, '--org'])
        for username, email in self.findall_regex(data, r'(.*) : (.*)'):
            yield Username(name=username, email=email)
            yield Email(address=email, username=username)
