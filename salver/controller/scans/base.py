# -*- coding: utf-8 -*-
from typing import List
from typing import Optional
import uuid

from pydantic import BaseModel

from salver.common import models
from salver.controller import exceptions
from salver.controller.services import agents_tasks
from salver.controller.services.agents import get_agents
from abc import ABC, abstractmethod, abstractproperty


class BaseScan(ABC):

    scan_id = None

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def configure(self, config: models.ScanConfig):
        """Configure the scan"""

    @abstractmethod
    def scan(self, facts):
        """Starts the scan"""

    def launch_collector(
        self, collector_name: str, facts: List[models.BaseFact], cb=None,
    ):
        def check_collector_exists(collector_name):
            for agent in get_agents().values():
                if collector_name in agent:
                    return
            raise exceptions.CollectorNotFound(collector_name)

        check_collector_exists(collector_name)

        agents_tasks.scan(
            self.scan_id, self.config.collector_name, facts, cb=cb,
        )
