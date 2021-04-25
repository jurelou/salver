# -*- coding: utf-8 -*-
import re

# from opulence.agent.collectors.dependencies import Dependency
from timeit import default_timer as timer
from typing import Dict, List, Union, Callable, Iterator, Optional
from functools import partial

from loguru import logger
from pydantic import BaseModel

from salver.common import models
from salver.common.utils import make_flat_list
from salver.common.limiter import Limiter, RequestRate
from salver.common.collectors.exceptions import (
    CollectorRuntimeError,
    InvalidCollectorDefinition,
)


class CollectorBaseConfig(BaseModel):
    name: str
    limiter: Optional[List[RequestRate]]

    class Config:
        use_enum_values = True


class BaseCollector:

    config: CollectorBaseConfig

    def __init__(self):
        self._callbacks: Dict[models.BaseFact, Callable] = self.callbacks()

        try:
            self.configure()
        except Exception as err:
            raise InvalidCollectorDefinition(type(self).__name__, err) from err

        self._limiter = None
        if self.config.limiter:
            self._limiter = Limiter(*self.config.limiter)

    def configure(self):
        self.config = CollectorBaseConfig(**self.config)

    def callbacks(self) -> Dict[models.BaseFact, Callable]:
        logger.warning(f'Collector {type(self)} does not have any callbacks')
        raise InvalidCollectorDefinition(
            type(self).__name__,
            f'Collector {type(self).__name__} does not have any callbacks',
        )

    def _sanitize_output(self, fn):
        try:

            output = make_flat_list(fn())
            if not output:
                return []
            for out in output:
                if isinstance(out, models.BaseFact):
                    yield out
                else:
                    logger.warning(
                        f'Found unknown output from collector {self.config.name}: {out}',
                    )
        except Exception as err:
            logger.error(
                f'Error while executing callback from {self.config.name}: {type(err).__name__} {err}',
            )
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

    def collect(self, facts: List[models.BaseFact]) -> models.CollectResult:
        if self._limiter:
            self._limiter.try_acquire()
        start_time = timer()

        callbacks = self._prepare_callbacks(facts)

        logger.debug(
            f'Execute collector {self.config.name} with \
            {len(facts)} facts and {len(callbacks)} callbacks',
        )

        output_facts = self._execute_callbacks(callbacks)
        return (
            models.CollectResult(
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
