# -*- coding: utf-8 -*-
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Waf(BaseFact):
    _name_ = "Waf"
    _description_ = "Web application firewall."
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.name = StringField(mandatory=True, default="Cloudflare")
        self.vendor = StringField()

    def get_summary(self):
        return f"{self.name.value}"
