# -*- coding: utf-8 -*-
import re

# from opulence.agent.collectors.dependencies import Dependency
from timeit import default_timer as timer
from typing import Dict, List, Union, Callable, Iterator, Optional
from functools import partial

from loguru import logger
from pydantic import BaseModel

from salver.common.facts import BaseFact

# from salver.common import models
from salver.common.utils import make_flat_list
from salver.common.limiter import Limiter, RequestRate
from salver.common.exceptions import CollectorRuntimeError, InvalidCollectorDefinition


class CollectorBaseConfig(BaseModel):
    name: str
    limiter: Optional[List[RequestRate]]

    class Config:
        use_enum_values = True


class BaseCollector:

    config: CollectorBaseConfig

    def __init__(self):
        self._callbacks: Dict[BaseFact, Callable] = self.callbacks()

        try:
            self.configure()
        except Exception as err:
            raise InvalidCollectorDefinition(
                collector_name=type(self).__name__, error=str(err)
            ) from err

        self.limiter = None
        if self.config.limiter:
            self.limiter = Limiter(self.config.name, *self.config.limiter)

    @property
    def callback_types(self):
        return [c.schema()["title"] for c in self.callbacks().keys()]

    def configure(self):
        self.config = CollectorBaseConfig(**self.config)

    def check_rate_limit(self):
        if self.limiter:
            self.limiter.try_acquire()
        else:
            logger.debug(f"no rate limit defined for {self.config.name}")

    def callbacks(self) -> Dict[BaseFact, Callable]:
        logger.warning(f"Collector {type(self)} does not have any callbacks")
        raise InvalidCollectorDefinition(
            collector_name=type(self).__name__,
            error=f"Collector does not have any callbacks",
        )

    def _sanitize_output(self, collect_id, fn):
        try:
            output = make_flat_list(fn())
            if not output:
                return
            for out in output:
                if isinstance(out, BaseFact):
                    yield out
                else:
                    error = (
                        f"Found unknown output from collector {self.config.name}: {out}"
                    )
                    # yield models.Error(
                    #     context=f"agent-collect.unknown_output",
                    #     collect_id=collect_id,
                    #     error=error,
                    #     collector_name=self.config.name
                    # )
                    logger.warning(error)

        except Exception as err:
            logger.error(
                f"Error while executing callback from {self.config.name}: {type(err).__name__} {err}",
            )
            raise CollectorRuntimeError(collector_name=self.config.name, error=err) from err
            # yield models.Error(
            #     context=f"agent-collect.error",
            #     error=str(err),
            #     collect_id=collect_id,
            #     collector_name=self.config.name
            # )

    def _prepare_callbacks(
        self,
        input_fact: Union[List[BaseFact], BaseFact],
    ) -> Iterator[Callable]:
        callbacks = []
        for cb_type, cb in self._callbacks.items():
            for fact in input_fact:
                if cb_type == type(fact):
                    callbacks.append(partial(cb, fact))
        return callbacks

    def collect(self, collect_id, facts: List[BaseFact]):
        self.check_rate_limit()

        callbacks = self._prepare_callbacks(facts)

        logger.debug(
            f"Execute collector {self.config.name} with \
            {len(facts)} facts and {len(callbacks)} callbacks",
        )

        for cb in callbacks:
            yield from self._sanitize_output(collect_id, cb)

    @staticmethod
    def findall_regex(data, regex):
        for item in re.findall(regex, data):
            if item:
                yield item
