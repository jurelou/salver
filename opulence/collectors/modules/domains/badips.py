import hashlib

import requests

from opulence import facts
from opulence.collectors.bases import HttpCollector


class BadIps(HttpCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "badips"
    _description_ = "check if ip is blacklisted. (ex: 91.133.35.36)"
    _author_ = "Henry"
    _version_ = 1
    _url_ = "https://www.badips.com/get/info/"

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = facts.IPv4

    def getLastReport(self, reports):
        return max([reports[k] for k in reports])

    def getProtocol(self, protocols, _id):
        for protocol in protocols:
            yield facts.Protocol(name=protocol, id=_id.hexdigest())

    def launch(self, fact):
        r = requests.get(self._url_ + fact.address.value).json()
        if "Listed" in r and r["Listed"] is True:
            _id = hashlib.sha1(fact.address.value.encode('utf-8'))
            LastReport = self.getLastReport(r['LastReport'])
            yield from self.getProtocol(r['Categories'], _id)
            yield facts.IPRanking(
                isBlacklisted=True,
                reportCount=r["ReporterCount"]["sum"],
                lastReport=LastReport,
                id=_id.hexdigest(),
            )
        else:
            yield facts.IPRanking(isBlacklisted=False)
