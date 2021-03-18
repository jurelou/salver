# -*- coding: utf-8 -*-
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Airline(BaseFact):
    _name_ = "airline"
    _description_ = "Represent a airline company"
    _author_ = "Henry"
    _version_ = 1

    def setup(self):
        self.name = StringField(mandatory=True)
        self.code_iata = StringField()
        self.code_icao = StringField()
        self.fullname = StringField()

    def get_summary(self):
        return f"{self.name.value}"
