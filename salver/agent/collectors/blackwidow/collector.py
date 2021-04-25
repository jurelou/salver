# -*- coding: utf-8 -*-

from salver.facts import Uri, Email, Phone, Domain
from salver.common.utils import get_actual_dir
from salver.common.collectors import DockerCollector


class BlackWidow(DockerCollector):
    config = {
        'name': 'blackwidow',
        'docker': {'build_context': get_actual_dir()},
    }

    def callbacks(self):
        return {
            Domain: self.scan,
        }

    def scan(self, domain):
        data = self.run_container(command=['-d', domain.fqdn, '-l', '5', '-v', 'y'])

        for email in self.findall_regex(data, r'Email found! (.*) '):
            yield Email(address=email)

        for number in self.findall_regex(data, r'Telephone # found! (.*) '):
            yield Phone(number=number)

        for url in self.findall_regex(
            data,
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]\
            {2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|\
            https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
        ):
            yield Uri(location=url)
