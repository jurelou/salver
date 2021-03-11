from loguru import logger

from opulence.common.fact import BaseFact
from opulence.common.factory import Factory
from opulence.engine.scans.base import BaseScan


class ScanFactory(Factory):
    def build(self):
        scans = {
            mod.name: mod
            for mod in self.load_classes_from_module("opulence/engine/scans", BaseScan)
        }
        self.items = scans
        logger.info(f"Loaded scans: {scans.keys()}")
        return scans
