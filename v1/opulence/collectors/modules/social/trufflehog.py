# -*- coding: utf-8 -*-
import json
import os
import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.common.utils import is_list
from opulence.facts import CryptoKey
from opulence.facts import GitRepository
from opulence.facts import Secret


class TruffleHog(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Truffle Hog"
    _description_ = "Find keys and secrets from public repositories."
    _author_ = "Henry"
    _version_ = 1
    _dependencies_ = [BinaryDependency("trufflehog")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = GitRepository

    ###############
    # Script attributes
    ###############
    _script_path_ = "trufflehog"
    _script_arguments_ = [
        "$GitRepository.url$",
        "--rules",
        os.path.dirname(__file__) + "/config/rulesRegex.json",
        "--regex",
        "--entropy=False",
        "--json",
    ]

    def launch(self, fact):
        if not is_list(fact):
            fact = [fact]
        args = self._find_and_replace_sigil(fact)
        stdout = self._exec(self.script_path, *args, ignore_error=True)
        return self.parse_result(stdout)

    def clear_secret(self, res, regex):
        for key in res["stringsFound"]:
            extracted = re.findall(regex, key)
            yield extracted[0].replace("'", "").replace('"', "")

    def parse_secret_found(self, res):
        if res["reason"] == "Generic_Secret" or res["reason"] == "Generic_API_Key":
            return list(self.clear_secret(res, r"['|\"][0-9a-zA-Z]{32,45}['|\"]"))
        if res["reason"] == "Twitter_OAuth" or res["reason"] == "Facebook_OAuth":
            return list(self.clear_secret(res, r"[\"\'][^ ]*[\"\']"))
        return res["stringsFound"]

    def duplicate(self, res, val, Final_Result):
        for final in Final_Result:
            if final.categorie.value == res["reason"]:
                if final._name_ == "Secret" and final.secret.value == val:
                    return True
                elif final._name_ == "CryptoKey" and final.key.value == val:
                    return True

    def Fact_selection(self, res, value):
        if value[:10] == "-----BEGIN":
            _categorie = re.findall(r"BEGIN (.*) PRIVATE", value)[0]
            return CryptoKey(key=value, categorie=_categorie)
        return Secret(secret=value, categorie=res["reason"])

    def parse_result(self, result):
        result_json = json.loads("[" + ",".join(result.split("\n")) + "]")
        Final_Result = []

        for res in result_json:
            res["stringsFound"] = self.parse_secret_found(res)
            for val in res["stringsFound"]:
                if len(val) > 4096 or self.duplicate(res, val, Final_Result):
                    continue

                Final_Result.append(self.Fact_selection(res, val))
        return Final_Result
