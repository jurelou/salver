# -*- coding: utf-8 -*-
from opulence.common.fields import IntegerField
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Port(BaseFact):
    _name_ = "Port"
    _description_ = "Represent an UDP or TCP network port and state"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.number = IntegerField(mandatory=True, default=80)
        self.state = StringField()
        self.transport = StringField()

    def get_summary(self):
        return f"{self.number.value}"
