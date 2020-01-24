import re

from opulence.collectors.bases.scriptCollector import ScriptCollector
from opulence.common.plugins.dependencies import (
    BinaryDependency, FileDependency
)
from opulence.facts import Domain


class GobusterDNS(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "GoBuster DNS"
    _description_ = "DNS subdomains brute force using gobuster."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [
        BinaryDependency("gobuster"),
        FileDependency("/srv/wordlists/directories-big.txt"),
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
        "dns",
        "--domain",
        "$Domain.fqdn$",
        "--wordlist",
        "/srv/wordlists/directories-big.txt",
        "--quiet",
        "--noprogress",
        "--showips",
    ]

    def parse_result(self, result):
        found_domains = re.findall("Found: (.*) \\[(.*)\\]\\n", result)
        if found_domains:
            for f in found_domains:
                domain, ip = f
                yield Domain(fqdn=domain, ip=ip)
