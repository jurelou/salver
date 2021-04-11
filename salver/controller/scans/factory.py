# -*- coding: utf-8 -*-
from loguru import logger

from salver.config import controller_config
from salver.common.factory import Factory
from salver.common.models.fact import BaseFact
from salver.controller.scans.base import BaseScan


class ScanFactory(Factory):
    def build(self):
        scans = {
            mod.name: mod
            for mod in self.load_classes_from_module(
                controller_config.salver.scans_path, BaseScan
            )
        }
        self.items = scans
        logger.info(f"Loaded scans: {scans.keys()}")
        return scans
