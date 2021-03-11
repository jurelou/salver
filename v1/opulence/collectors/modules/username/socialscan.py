import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Email, SocialProfile, Username


class Socialscan(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Socialscan"
    _description_ = "Find accounts from a given username/email"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("socialscan")]

    ###############
    # Collector attributes
    ###############
    _active_scanning_ = False
    _allowed_input_ = (Username, Email)

    ###############
    # Script attributes
    ###############
    _script_path_ = "socialscan"

    def launch(self, fact):
        if isinstance(fact, Username):
            command = [
                self._script_path_,
                fact.name.value,
                "-v",
                "--platforms",
                "twitter",
                "github",
                "tumblr",
                "snapchat",
                "gitlab",
                "reddit",
                "yahoo",
            ]
        elif isinstance(fact, Email):
            command = [
                self._script_path_,
                fact.address.value,
                "-v",
                "--platforms",
                "twitter",
                "github",
                "tumblr",
                "lastfm",
                "pinterest",
                "spotify",
            ]
        yield from self.parse_result(self._exec(*command))

    def parse_result(self, result):
        profiles = re.findall("Checked *(.*?) *on *(.*?) *: (?!Available)", result)
        if profiles:
            for profile in profiles:
                username, website = profile
                yield SocialProfile(username=username, site=website)
