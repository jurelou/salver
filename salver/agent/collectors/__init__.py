from .factory import CollectorFactory
from .base import BaseCollector

all_collectors = CollectorFactory().build()

__all__ = ["all_collectors", "BaseCollector"]
