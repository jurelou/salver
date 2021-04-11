# -*- coding: utf-8 -*-
import uuid
from abc import ABC, abstractmethod, abstractproperty
from typing import List, Optional

from pydantic import BaseModel

from salver.controller import exceptions
from salver.common.models import BaseFact, ScanConfig
from salver.controller.services import agents_tasks
from salver.controller.services.agents import get_collectors_names


class BaseScan(ABC):

    scan_id = None

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def configure(self, config: ScanConfig):
        """Configure the scan"""

    @abstractmethod
    def scan(self, facts):
        """Starts the scan"""

    def launch_collector(
        self,
        collector_name: str,
        facts: List[BaseFact],
        cb=None,
    ):

        print("===========", get_collectors_names())
        if collector_name not in get_collectors_names():
            raise exceptions.CollectorNotFound(collector_name)

        agents_tasks.scan(
            self.scan_id,
            self.config.collector_name,
            facts,
            cb=cb,
        )
