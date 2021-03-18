# -*- coding: utf-8 -*-
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Organization(BaseFact):
    _name_ = "Organization"
    _description_ = "Represent an organization details"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.name = StringField(mandatory=True, default="Alphabet")

    def get_summary(self):
        return f"{self.name.value}"
