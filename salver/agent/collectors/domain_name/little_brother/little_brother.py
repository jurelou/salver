# -*- coding: utf-8 -*-

from salver.common.facts import Email, Domain
from salver.common.utils import get_actual_dir
from salver.agent.collectors import DockerCollector


class LittleBrother(DockerCollector):
    config = {
        'name': 'little-brother',
        'docker': {'build_context': get_actual_dir()},
    }

    def callbacks(self):
        return {Domain: self.scan}

    def scan(self, domain):
        data = self.run_container(command=['--domain', domain.fqdn, '-v', '1'])
        for item in self.findall_regex(data, r'Email: (.*) \('):
            yield Email(address=item)