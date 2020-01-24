import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import CVE, Domain, IPv4, VulDB


class NmapNSE(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Nmap nse"
    _description_ = "Nmap vulnerability scan using vulscan (VulDB)"
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
        "--script",
        "vulscan",  # "--script-args", "vulscandb=exploitdb.csv,cve.csv,scipvuldb.csv",
        "-sV",
        "-oX",
        "-",
        "$Domain.fqdn$",
        "$IPv4.address$",
    ]

    def parse_result(self, result):
        nse_results = re.findall('<script id="vulscan" output="(.*)/>', result)
        for i in nse_results:
            entries_vulscan = re.findall("\\[([\\d]{4,10})] (.*?)&#xa", i)
            entries_cve = re.findall("\\[CVE-(.*?)\\] (.*?)&", i)
            if entries_cve:
                for entry in entries_cve:
                    _id, description = entry
                    yield CVE(id="CVE-{}".format(_id), description=description)
            if entries_vulscan:
                for entry in entries_vulscan:
                    _id, description = entry
                    yield VulDB(id=int(_id), description=description)
