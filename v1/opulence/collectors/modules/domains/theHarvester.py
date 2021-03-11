import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain, IPv4


class TheHarvester(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "TheHarvester"
    _description_ = "Gather company domain from public sources."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("theHarvester")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Domain
    _active_scanning_ = False

    ###############
    # Script attributes
    ###############
    _script_path_ = "theHarvester"
    _script_arguments_ = [
        "--domain",
        "$Domain.fqdn$",
        "-b",
        "baidu,bing,certspotter,crtsh,dnsdumpster,dogpile,duckduckgo,google,intelx,linkedin,linkedin_links,netcraft,otx,threatcrowd,trello,twitter,vhost,virustotal,yahoo",  # noqa: E501
    ]

    def parse_result(self, result):
        found_ips = re.search(
            "\\[\\*\\] IPs found: \\d*\\n-------------------\\n((.|\\n)*?)\\[\\*\\]",
            result,
        )
        found_domains = re.search(
            "\\[\\*\\] Hosts found: \\d*\\n---------------------\\n((.|\\n)*)\\n\\[\\*\\]",  # noqa: E501
            result,
        )

        if found_domains and found_domains.group(1):
            domains_ip = re.findall(
                "(.*):(\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b)?",
                found_domains.group(1),
            )
            if domains_ip:
                for d in domains_ip:
                    domain, ip = d
                    yield Domain(fqdn=domain, ip=ip)

        if found_ips and found_ips.group(1):
            ips = re.findall(
                "(\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b)", found_ips.group(1),
            )
            if ips:
                for i in ips:
                    yield IPv4(address=i)
