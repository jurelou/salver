<<<<<<< HEAD
# -*- coding: utf-8 -*-
from .base import BaseScan
from .full_scan import FullScan
from .single_collector import SingleCollector

all_scans = [SingleCollector, FullScan]

__all__ = ['BaseScan', 'all_scans']
=======
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
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
