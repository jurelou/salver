# -*- coding: utf-8 -*-
import uuid

from salver.common.models import BaseFact, ScanConfig


class BaseScan:

    name: str = ""
    config: ScanConfig

    def __init__(self):
        if not self.name:
            print("NO NAME")
            raise ValueError(f'Scan {type(self).__name__} does not have a `name` property')
        self.external_id : uuid.UUID = uuid.uuid4()

    def configure(self, config: ScanConfig):
        self.config = config

    def scan(self, facts):
        """Starts the scan"""
        raise NotImplementedError(f"Scan {self.name} does not implements a `scan` method.")

    # def launch_collector(
    #     self,
    #     collector_name: str,
    #     facts: List[BaseFact],
    #     cb=None,
    # ):
    #     if collector_name not in get_collectors_names():
    #         raise exceptions.CollectorNotFound(collector_name)

    #     agents_tasks.scan(
    #         self.scan_id,
    #         self.config.collector_name,
    #         facts,
    #         cb=cb,
    #     )
