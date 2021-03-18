# -*- coding: utf-8 -*-
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class URI(BaseFact):
    _name_ = "URI"
    _description_ = "Uniform Resource Locators (RFC 1738)"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.full_uri = StringField(mandatory=True, default="http://google.fr?q=42#42")
        self.sheme = StringField()
        self.authority = StringField()
        self.path = StringField()
        self.query = StringField()
        self.fragment = StringField()

    def get_summary(self):
        return f"{self.full_uri.value}"
