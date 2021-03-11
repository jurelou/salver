from loguru import logger

from opulence.common.fact import BaseFact
from opulence.common.factory import Factory


class FactFactory(Factory):
    def build(self):
        facts = {
            mod.schema()["title"]: mod
            for mod in self.load_classes_from_module("opulence/facts", BaseFact)
        }
        self.items = facts
        logger.info(f"Loaded facts: {facts.keys()}")
        return facts
