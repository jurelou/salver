import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import SocialProfile, Username


class Profiler(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Profiler"
    _description_ = "OSINT HUMINT Profile Collector"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("recon-ng")]

    ###############
    # Collector attributes
    ###############
    _active_scanning_ = False
    _allowed_input_ = Username

    ###############
    # Script attributes
    ###############
    _script_path_ = "recon-ng"
    _script_arguments_ = [
        "-m",
        "recon/profiles-profiles/profiler",
        "-o",
        "SOURCE=$Username.name$",
        "-x",
    ]

    def parse_result(self, result):
        results = []
        found_social_profiles = re.findall(
            "(.*)\\[profile\\] (.*) - (.*) \\((.*)\\)", result
        )
        if not found_social_profiles:
            return results
        for f in found_social_profiles:
            _, username, site, url = f
            results.append(SocialProfile(username=username, url=url, site=site))
        return results
