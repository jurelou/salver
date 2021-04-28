# -*- coding: utf-8 -*-
from salver.facts import Profile, Username
from salver.common.utils import get_actual_dir
from salver.common.collectors import DockerCollector


class Sherlock(DockerCollector):
    config = {
        'name': 'sherlock',
        'docker': {'build_context': get_actual_dir()},
    }

    def callbacks(self):
        return {Username: self.from_username}

    def from_username(self, username):
        data = self.run_container(
            command=[username.name, '--no-color', '--print-found', '--timeout', '20'],
        )
        for item in self.findall_regex(data, r'\[\+\] .*: (.*)\n'):
            yield Profile(url=item)