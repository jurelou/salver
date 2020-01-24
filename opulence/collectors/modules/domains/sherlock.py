import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import SocialProfile, Username


class Sherlock(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Sherlock"
    _description_ = "Find usernames across social networks"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("sherlock")]

    ###############
    # Collector attributes
    ###############
    _active_scanning_ = False
    _allowed_input_ = Username

    ###############
    # Script attributes
    ###############
    _script_path_ = "sherlock"

    def launch(self, fact):
        cmd = [
            self._script_path_,
            fact.name.value,
            "--print-found",
            "--folderoutput",
            "/tmp",
        ]
        yield from self.parse_result(self._exec(*cmd), fact.name.value)

    def parse_result(self, result, username):
        found_social_profiles = re.findall("\\[\\+\\] (.*): (.*)", result)
        if found_social_profiles:
            for f in found_social_profiles:
                site, url = f
                yield SocialProfile(username=username, site=site, url=url)
