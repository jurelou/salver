from loguru import logger

from salver.common.facts import BaseFact
from salver.common.factory import Factory


class FactFactory(Factory):
    def build(self):
        facts = {
            mod.schema()["title"]: mod
            for mod in self.load_classes_from_module("salver/common/facts", BaseFact)
        }
        self.items = facts
        logger.info(f"Loaded {len(facts.keys())} facts: {list(facts.keys())}")
        return facts
