# -*- coding: utf-8 -*-
import uuid
from typing import List
from salver.common.models import BaseFact, ScanConfig, Collect
from salver.engine.exceptions import CollectorNotFound

class BaseScan:

    name: str = ""
    config: ScanConfig

    def __init__(self, agents_collectors_producers):
        if not self.name:
            print("NO NAME")
            raise ValueError(f'Scan {type(self).__name__} does not have a `name` property')

        self.agents_collectors_producers = agents_collectors_producers
        self.external_id : uuid.UUID = uuid.uuid4()

    def configure(self, config: ScanConfig):
        self.config = config

    def scan(self, facts):
        """Starts the scan"""
        raise NotImplementedError(f"Scan {self.name} does not implements a `scan` method.")

    def launch_collector(
        self,
        collector_name: str,
        facts: List[BaseFact],
    ):
        if collector_name not in self.agents_collectors_producers:
            raise CollectorNotFound(collector_name)

        self.agents_collectors_producers[collector_name].produce(
            Collect(
                scan_id=self.external_id,
                collector_name=collector_name,
                facts=facts
            )
        )
