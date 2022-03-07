# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from uuid import uuid4
from typing import List

from loguru import logger

from salver.common.facts import BaseFact
from salver.engine.controllers import agent_tasks

from salver.engine.tasks import launch_scan

class ScanStrategy(ABC):
    def run_agent_scan(self, facts: List[BaseFact], collector_name: str = None):
        scan_id = uuid4()
        launch_scan.apply_async(kwargs={'collector_name': collector_name, 'scan_id': scan_id, 'facts': facts})
        return scan_id

    @abstractmethod
    def run(self, facts: List[BaseFact]):
        pass


class Scan:
    def __init__(self, strategy: ScanStrategy = None) -> None:
        self._strategy = strategy

    def run(self, facts: List[BaseFact]):
        if not self._strategy:
            logger.critical("No ScanStrategy defined.")
            raise ValueError()
        self._strategy.run(facts)


"""
class BaseScan:

    name: str = ""
    config: ScanConfig
-
    def __init__(self, agents_collectors_producers):
        if not self.name:
            print("NO NAME")
            raise ValueError(f'Scan {type(self).__name__} does not have a `name` property')

        self.agents_collectors_producers = agents_collectors_producers

    @property
    def external_id(self):
        return self._external_id

    @external_id.setter
    def external_id(self, id):
        self._external_id = id

    def configure(self, config: ScanConfig):
        self.config = config

    def scan(self, facts):
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
"""
