import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain, IPv4, OperatingSystem


class NmapOSScan(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Nmap OS scan"
    _description_ = "Performs nmap OS detection"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("nmap")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = (Domain, IPv4)
    _active_scanning_ = False

    ###############
    # Script attributes
    ###############
    _script_path_ = "nmap"
    _script_arguments_ = [
        "-O",
        "--osscan-guess",
        "-oX",
        "-",
        "$Domain.fqdn$",
        "$IPv4.address$",
    ]

    def parse_result(self, result):
        found_os = re.findall(
            '<osclass type="(.+?)" vendor="(.+?)" osfamily="(.+?)" osgen="(.+?)" accuracy="(.+?)">',  # NOQA
            result,
        )
        if not found_os:
            return
        res = []
        for os in found_os:
            _, vendor, osfamily, osgen, accuracy = os
            res.append(
                OperatingSystem(
                    family=osfamily, version=osgen, vendor=vendor, weight=accuracy
                )
            )
        return res
