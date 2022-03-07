# -*- coding: utf-8 -*-
from loguru import logger

from salver.common.facts import IPv4, Email, Domain, Company
from salver.common.utils import get_actual_dir
from salver.agent.collectors import DockerCollector


class TheHarvester(DockerCollector):
    config = {
        "name": "the-harvester",
        "docker": {"build_context": get_actual_dir()},
    }

    def callbacks(self):
        return {
            Domain: self.from_domain,
        }

    def from_domain(self, domain):
        yield from self.scan(domain.fqdn)

    def scan(self, target):
        data = self.run_container(
            command=[
                "-d",
                target,
                "--source",
                "anubis,baidu,bing,bufferoverun,certspotter,crtsh,dnsdumpster,duckduckgo,google,hackertarget,linkedin,linkedin_links,n45ht,omnisint,qwant,rapiddns,threatcrowd,threatminer,trello,twitter,urlscan,yahoo",
            ],
        )

        for item, _ in self.findall_regex(
            data,
            r"\[\*\] IPs found: \d+\n-------------------\n((.|\n)*)\n\[\*\] Emails found",
        ):
            for ip in item.split("\n"):
                if ip:
                    yield from [ IPv4(address=i.strip()) for i in ip.split(",")]

        for item, _ in self.findall_regex(
            data,
            r"\[\*\] Emails found: \d+\n----------------------\n((.|\n)*)\n\[\*\] Hosts found",
        ):
            for email in item.split("\n"):
                if email:
                    yield Email(address=email)

        for item, _ in self.findall_regex(
            data,
            r"\[\*\] Hosts found: \d+\n---------------------\n((.|\n)*)",
        ):
            for host in item.split("\n"):
                if not host:
                    continue
                if ":" in host:
                    domain, ip = host.split(":")
                    yield Domain(fqdn=domain, address=ip)
                    yield from [ IPv4(address=i.strip(), domain=domain) for i in ip.split(",")]
                else:
                    yield Domain(fqdn=host)
