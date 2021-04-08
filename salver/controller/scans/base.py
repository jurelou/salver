# -*- coding: utf-8 -*-
import uuid
from abc import ABC, abstractmethod, abstractproperty
from typing import List, Optional

from pydantic import BaseModel

from salver.controller import models, exceptions
from salver.common.models import BaseFact
from salver.controller.services import agents_tasks
from salver.controller.services.agents import get_agents


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
        self,
        collector_name: str,
        facts: List[BaseFact],
        cb=None,
    ):
        def check_collector_exists(collector_name):
            for agent in get_agents().values():
                if collector_name in agent:
                    return
            raise exceptions.CollectorNotFound(collector_name)

        check_collector_exists(collector_name)

        agents_tasks.scan(
            self.scan_id,
            self.config.collector_name,
            facts,
            cb=cb,
        )
