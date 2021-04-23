# -*- coding: utf-8 -*-
from loguru import logger

from salver.common.factory import Factory
from salver.common.models.fact import BaseFact


class FactFactory(Factory):
    def build(self):
        facts = {
            mod.schema()["title"]: mod
            for mod in self.load_classes_from_module("salver/facts/modules/", BaseFact)
        }
        self.items = facts
        return facts
