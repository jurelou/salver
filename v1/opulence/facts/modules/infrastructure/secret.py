# -*- coding: utf-8 -*-
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Secret(BaseFact):
    _name_ = "Secret"
    _description_ = "Represent a secret or key"
    _author_ = "Henry"
    _version_ = 1

    def setup(self):
        self.secret = StringField(mandatory=True, default="0xdeadbeef")
        self.categorie = StringField()

    def get_summary(self):
        return f"{self.secret.value}"
