# -*- coding: utf-8 -*-
from functools import partial
import re

# from opulence.agent.collectors.dependencies import Dependency
from timeit import default_timer as timer
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union
import json
from loguru import logger
from pydantic import BaseModel
from pydantic import ValidationError
from pydantic import root_validator

from opulence.agent.exceptions import CollectorRuntimeError
from opulence.agent.exceptions import InvalidCollectorDefinition
from opulence.common import models
from opulence.common.types import BaseSet
from opulence.common.utils import make_list
from opulence.common.limiter import Limiter, RequestRate

# class CollectItem(BaseModel):
#     pass

# class Schedule(BaseModel):
#     minute: Union[str, int] = "*"
#     hour: Union[str, int] = "*"
#     day_of_week: Union[str, int] = "*"
#     day_of_month: Union[str, int] = "*"
#     month_of_year: Union[str, int] = "*"


class BaseConfig(BaseModel):
    name: str
    limiter: Optional[List[RequestRate]]

    class Config:
        use_enum_values = True
    # periodic: bool = False
    # schedule: Optional[Schedule] = None

    # @root_validator
    # def check_schedule(cls, values):
    #     is_periodic = values.get('periodic')
    #     if is_periodic:
    #         if not values.get('schedule'):
    #             raise ValueError(f'Schedule should be set for collector {values.get("name")}')
    #     return values



class BaseCollector:

    config: BaseConfig
    # dependencies: Optional[List[Dependency]] = None

    def __init__(self):
        self._callbacks: Dict[Union[models.BaseFact, BaseSet], Callable] = self.callbacks()

        try:
            self.configure()
        except ValidationError as err:
            raise InvalidCollectorDefinition(self.config.name, err) from err

        self._limiter = None
        if self.config.limiter:
            self._limiter = Limiter(*self.config.limiter)

    def configure(self):
        self.config = BaseConfig(**self.config)

    def check_rate_limit(self):
        if not self._limiter:
            print("no rate limit")
            return
        self._limiter.try_acquire()

    def callbacks(self) -> Dict[Union[models.BaseFact, BaseSet], Callable]:
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
        self, input_fact: Union[List[models.BaseFact], models.BaseFact],
    ) -> Iterator[Callable]:
        callbacks = []
        for cb_type, cb in self._callbacks.items():
            if isinstance(cb_type, BaseSet):
                _set = cb_type.select_from(input_fact)
                if _set:
                    callbacks.append(partial(cb, _set))
            else:
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
        return models.ScanResult(
            duration=timer() - start_time,
            executions_count=len(callbacks),
            facts=[ f.hash__ for f in output_facts],
        ), output_facts

    @staticmethod
    def findall_regex(data, regex):
        for item in re.findall(regex, data):
            if item:
                yield item
