# -*- coding: utf-8 -*-

from salver.facts import IPv4, Domain, Socket
from salver.common.utils import get_actual_dir
from salver.common.collectors import DockerCollector


class Nmap(DockerCollector):
    config = {
        'name': 'nmap',
        'docker': {'build_context': get_actual_dir()},
    }

    def callbacks(self):
        return {
            Domain: self.from_domain,
            IPv4: self.from_ip,
        }

    def _scan(self, target):
        data = self.run_container(command=['-oX', '-', '-sS', '-T3', target])
        yield
        for proto, port, service in self.findall_regex(
            data,
            r'port protocol="(.*)" portid="(.*)"><state \
            state=.* reason=.*service name="(.*)" method=',
        ):
            yield Socket(proto=proto, port=port, service_name=service)

    def from_domain(self, domain):
        yield from self._scan(domain.fqdn)

    def from_ip(self, ip):
        yield from self._scan(ip.address)
