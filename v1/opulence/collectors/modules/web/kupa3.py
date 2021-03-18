# -*- coding: utf-8 -*-
import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain
from opulence.facts import File


class Kupa3(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Kupa3"
    _description_ = "Extract javascript files and trackers."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("kupa3")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Domain

    ###############
    # Script attributes
    ###############
    _script_path_ = "kupa3"

    def launch(self, fact):
        commands = [
            [self._script_path_, f"http://{fact.fqdn.value}"],
            [self._script_path_, f"https://{fact.fqdn.value}"],
        ]

        for command in commands:
            yield from self.parse_result(self._exec(*command))

    def parse_result(self, result):
        links = re.findall("LINK->(.*)\\n", result)
        scripts = re.findall("SCRIPT-> (.*)\\n", result)

        if links:
            for link in links:
                yield Domain(fqdn=link)
        if scripts:
            for script in scripts:
                yield File(filename=script.split("/")[-1], url=script, extension="js")
