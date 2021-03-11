from opulence.common.fields import BooleanField
from opulence.common.fields import IntegerField
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class IPv4(BaseFact):
    _name_ = "IPv4"
    _description_ = "Represent an IP address version 4"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.address = StringField(mandatory=True, default="127.0.0.1")

    def get_summary(self):
        return f"{self.address.value}"


class IPv6(BaseFact):
    _name_ = "IPv6"
    _description_ = "Represent an IP address version 6"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.address = StringField(mandatory=True, default="127.0.0.1")

    def get_summary(self):
        return f"{self.address.value}"


class IPRanking(BaseFact):
    _name_ = "IPRanking"
    _description_ = "Represent IP's reputation"
    _author_ = "Henry"
    _version_ = 1

    def setup(self):
        self.isBlacklisted = BooleanField(mandatory=True, default=False)
        self.reportCount = IntegerField()
        self.lastReport = IntegerField()
        self.id = StringField()

    def get_summary(self):
        return f"{self.isBlacklisted.value}"
