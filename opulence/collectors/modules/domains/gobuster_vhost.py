import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import (
    BinaryDependency, FileDependency
)
from opulence.facts import Domain


class GobusterVhost(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "GoBuster Vhost"
    _description_ = "Virtual host brute force using gobuster."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [
        BinaryDependency("gobuster"),
        FileDependency("/srv/wordlists/subdomains-1000.txt"),
    ]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Domain

    ###############
    # Script attributes
    ###############
    _script_path_ = "gobuster"
    _script_arguments_ = [
        "vhost",
        "--url",
        "$Domain.fqdn$",
        "--wordlist",
        "/srv/wordlists/subdomains-1000.txt",
        "--quiet",
        "--noprogress",
        "--insecuressl",
    ]

    def parse_result(self, result):
        found_domains = re.findall("Found: (.*) \\(Status:", result)
        if found_domains:
            for f in found_domains:
                yield Domain(fqdn=f)
