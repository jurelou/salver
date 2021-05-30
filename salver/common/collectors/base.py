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

        self.limiter = None
        if self.config.limiter:
            self.limiter = Limiter(self.config.name, *self.config.limiter)

    @property
    def callback_types(self):
        return [c.schema()['title'] for c in self.callbacks().keys()]

    def configure(self):
        self.config = CollectorBaseConfig(**self.config)

    def callbacks(self) -> Dict[models.BaseFact, Callable]:
        logger.warning(f'Collector {type(self)} does not have any callbacks')
        raise InvalidCollectorDefinition(
            type(self).__name__,
            f'Collector {type(self).__name__} does not have any callbacks',
        )

    def _sanitize_output(self, collect_id, fn):
        try:
            output = make_flat_list(fn())
            if not output:
                return
            for out in output:
                if isinstance(out, models.BaseFact):
                    yield out
                else:
                    error = (
                        f'Found unknown output from collector {self.config.name}: {out}'
                    )
                    yield models.Error(
                        context=f'agent-collect.unknown_output',
                        collect_id=collect_id,
                        error=error,
                        collector_name=self.config.name,
                    )
                    logger.warning(error)

        except Exception as err:
            logger.error(
                f'Error while executing callback from {self.config.name}: {type(err).__name__} {err}',
            )
            yield models.Error(
                context=f'agent-collect.error',
                error=str(err),
                collect_id=collect_id,
                collector_name=self.config.name,
            )

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

    def collect(self, collect_id, facts: List[models.BaseFact]):
        callbacks = self._prepare_callbacks(facts)

        for cb in callbacks:
            yield from self._sanitize_output(collect_id, cb)

    @staticmethod
    def findall_regex(data, regex):
        for item in re.findall(regex, data):
            if item:
                yield item
