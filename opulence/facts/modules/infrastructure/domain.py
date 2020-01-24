from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Domain(BaseFact):
    _name_ = "Domain name"
    _description_ = "Represent a domain name"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.fqdn = StringField(mandatory=True, default="example.com")
        self.whois = StringField()
        self.ip = StringField()

    def get_summary(self):
        return "{}".format(self.fqdn.value)
