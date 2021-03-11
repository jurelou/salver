from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class CPE(BaseFact):
    _name_ = "CPE"
    _description_ = "Common platform enumeration (nist)"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.id = StringField(mandatory=True, default="cpe:2.3:a:apache:5.0.0:*")

    def get_summary(self):
        return f"{self.id.value}"
