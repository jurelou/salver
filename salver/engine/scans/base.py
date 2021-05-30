# -*- coding: utf-8 -*-
import uuid
from typing import List
<<<<<<< HEAD

from salver.common.models import Collect, BaseFact, ScanConfig
from salver.engine.exceptions import CollectorNotFound


class BaseScan:

    name: str = ''
=======
from salver.common.models import BaseFact, ScanConfig, Collect
from salver.engine.exceptions import CollectorNotFound

class BaseScan:

    name: str = ""
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
    config: ScanConfig

    def __init__(self, agents_collectors_producers):
        if not self.name:
<<<<<<< HEAD
            err = f'Scan {type(self).__name__} does not have a `name` property'
            logger.error(err)
            raise ValueError(err)
=======
            print("NO NAME")
            raise ValueError(f'Scan {type(self).__name__} does not have a `name` property')
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

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
        """Starts the scan"""
<<<<<<< HEAD
        raise NotImplementedError(
            f'Scan {self.name} does not implements a `scan` method.',
        )
=======
        raise NotImplementedError(f"Scan {self.name} does not implements a `scan` method.")
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

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
<<<<<<< HEAD
                facts=facts,
            ),
=======
                facts=facts
            )
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
        )
