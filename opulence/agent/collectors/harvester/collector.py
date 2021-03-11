import re

from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.company import Company
from opulence.facts.domain import Domain
from opulence.facts.email import Email
from opulence.facts.ipv4 import IPv4


class TheHarester(DockerCollector):
    config = {
        "name": "harvester",
        "docker": {"build_context": get_actual_dir()},
    }

    def callbacks(self):
        return {
            Domain: self.from_domain,
            Company: self.from_company,
        }

    def from_company(self, company):
        yield from self.scan(company.name)

    def from_domain(self, domain):
        yield from self.scan(domain.fqdn)

    def scan(self, target):
        data = self.run_container(
            command=[
                "-d",
                target,
                "--source",
                "baidu,bing,bufferoverun,certspotter,crtsh,dnsdumpster,duckduckgo,exalead,google,linkedin,linkedin_links,netcraft,omnisint,otx,qwant,rapiddns,threatminer,twitter,urlscan,yahoo",
            ],
        )

        for item, _ in self.findall_regex(
            data,
            r"\[\*\] IPs found: \d+\n-------------------\n((.|\n)*)\n\[\*\] Emails found",
        ):
            for ip in item.split("\n"):
                if ip:
                    yield IPv4(address=ip)

        for item, _ in self.findall_regex(
            data,
            r"\[\*\] Emails found: \d+\n----------------------\n((.|\n)*)\n\[\*\] Hosts found",
        ):
            for email in item.split("\n"):
                if email:
                    yield Email(address=email)

        for item, _ in self.findall_regex(
            data, r"\[\*\] Hosts found: \d+\n---------------------\n((.|\n)*)"
        ):
            for host in item.split("\n"):
                if not host:
                    continue
                if ":" in host:
                    domain, ip = host.split(":")
                    yield Domain(fqdn=domain, address=ip)
                    yield IPv4(address=ip, dns=domain)
                else:
                    yield Domain(fqdn=host)
