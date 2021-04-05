# -*- coding: utf-8 -*-
from salver.agent.collectors.docker import DockerCollector
from salver.common.utils import get_actual_dir
from salver.facts import Domain


class Subfinder(DockerCollector):
    config = {
        "name": "subfinder",
        "docker": {"build_context": get_actual_dir()},
    }

    def callbacks(self):
        return {Domain: self.scan}

    def scan(self, domain):
        data = self.run_container(command=["-d", domain.fqdn, "-nC", "-silent"])
        for domain in data.split("\n"):
            yield Domain(fqdn=domain)
