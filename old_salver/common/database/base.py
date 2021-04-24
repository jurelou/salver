# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class BaseDB(ABC):
    @abstractmethod
    def flush(self) -> None:
        pass

    @abstractmethod
    def bootstrap(self) -> None:
        pass
