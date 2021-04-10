# -*- coding: utf-8 -*-
import re
import json

# from opulence.agent.collectors.dependencies import Dependency
from timeit import default_timer as timer
from typing import Dict, List, Union, Callable, Iterator, Optional
from functools import partial

from loguru import logger
from pydantic import BaseModel, ValidationError, root_validator

from salver.common import models
from salver.common.utils import make_list
from salver.common.limiter import Limiter, RequestRate
from salver.agent.exceptions import CollectorRuntimeError, InvalidCollectorDefinition

# class Schedule(BaseModel):
#     minute: Union[str, int] = "*"
#     hour: Union[str, int] = "*"
#     day_of_week: Union[str, int] = "*"
#     day_of_month: Union[str, int] = "*"
#     month_of_year: Union[str, int] = "*"



class BaseCollector:

    config: models.CollectorBaseConfig
    # dependencies: Optional[List[Dependency]] = None

    def __init__(self):
        self._callbacks: Dict[models.BaseFact, Callable] = self.callbacks()

        try:
            self.configure()
        except ValidationError as err:
            raise InvalidCollectorDefinition(self.config.name, err) from err

        self._limiter = None
        if self.config.limiter:
            self._limiter = Limiter(*self.config.limiter)

    def configure(self):
        self.config = models.CollectorBaseConfig(**self.config)

    def check_rate_limit(self):
        if not self._limiter:
            print("no rate limit")
            return
        self._limiter.try_acquire()

    def callbacks(self) -> Dict[models.BaseFact, Callable]:
        raise InvalidCollectorDefinition(
            self.config.name,
            f"Collector {type(self).__name__} does not have any callbacks",
        )

    def _sanitize_output(self, fn):
        try:
            output = make_list(fn())
            output = list(filter(None, output))
            if not output:
                return []
            for out in output:
                if isinstance(out, models.BaseFact):
                    yield out
                else:
                    logger.error(
                        f"Found unknown output from collector {self.config.name}: {out}",
                    )
        except Exception as err:
            logger.error(f"Error while executing {fn} from {self.config.name}: {err}")
            raise CollectorRuntimeError(self.config.name, err) from err

    def _prepare_callbacks(
        self,
        input_fact: Union[List[models.BaseFact], models.BaseFact],
    ) -> Iterator[Callable]:
        callbacks = []
        for cb_type, cb in self._callbacks.items():
            for fact in input_fact:
                if cb_type == type(fact):
                    callbacks.append(partial(cb, fact))
        return callbacks

    def _execute_callbacks(self, callbacks):
        facts = []
        for cb in callbacks:
            facts.extend(list(self._sanitize_output(cb)))
        return facts

    def collect(self, facts: List[models.BaseFact]) -> models.ScanResult:
        start_time = timer()

        callbacks = self._prepare_callbacks(facts)

        logger.info(
            f"Execute collector {self.config.name} with {len(facts)} facts and {len(callbacks)} callbacks",
        )

        output_facts = self._execute_callbacks(callbacks)
        return (
            models.ScanResult(
                duration=timer() - start_time,
                executions_count=len(callbacks),
                facts=[f.hash__ for f in output_facts],
            ),
            output_facts,
        )

    @staticmethod
    def findall_regex(data, regex):
        for item in re.findall(regex, data):
            if item:
                yield item
