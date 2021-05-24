from .base import BaseScan

from .single_collector import SingleCollector
from .full_scan import FullScan

all_scans = [
    SingleCollector,
    FullScan
]

__all__= [
    "BaseScan",
    'all_scans'
]