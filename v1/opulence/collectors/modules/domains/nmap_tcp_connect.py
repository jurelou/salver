import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain, IPv4, Port


class NmapTCPConnect(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Nmap TCP connect"
    _description_ = "Performs nmap TCP connect scan (-sT)"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("nmap")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = (Domain, IPv4)
    _active_scanning_ = True

    ###############
    # Script attributes
    ###############
    _script_path_ = "nmap"
    _script_arguments_ = ["-sT", "-oX", "-", "$Domain.fqdn$", "$IPv4.address$"]

    def parse_result(self, result):

        found_ports = re.findall(
            'protocol="(.+?)" portid="(.+?)"><state state="(.+?)"', result
        )
        if not found_ports:
            return
        res = []
        for port in found_ports:
            proto, port_number, state = port
            res.append(Port(number=port_number, state=state, transport=proto))
        return res
