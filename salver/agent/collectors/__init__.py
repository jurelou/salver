from .base import BaseCollector, CollectorBaseConfig
from .docker import DockerCollector
from .factory import CollectorFactory

all_collectors = CollectorFactory().build()

__all__ = [
    "all_collectors",
    "BaseCollector",
    "CollectorBaseConfig",
    "DockerCollector"
]
