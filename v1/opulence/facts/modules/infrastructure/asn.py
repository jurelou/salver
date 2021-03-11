from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class ASN(BaseFact):
    _name_ = "ASN"
    _description_ = r"""
        A unique ASN is allocated to each autonomous system for use in BGP routing.
        ASNs are important because the ASN uniquely identifies \
        each network on the Internet.
        """
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.id = StringField(mandatory=True, default="AS8426")
        self.organization = StringField()

    def get_summary(self):
        return f"{self.id.value}"
