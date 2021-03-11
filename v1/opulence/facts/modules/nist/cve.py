from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class CVE(BaseFact):
    _name_ = "CVE"
    _description_ = "Common vulnerabilities exposures identifier standart (nist)"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.id = StringField(mandatory=True, default="CVE-2019-9815")
        self.description = StringField()

    def get_summary(self):
        return "{}".format(self.id.value)
