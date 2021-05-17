from .base import BaseScan

from .single_collector import SingleCollector

all_scans = [
    SingleCollector
]
__all__= [
    "BaseScan",
    'all_scans'
]