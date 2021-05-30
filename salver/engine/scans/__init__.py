# -*- coding: utf-8 -*-
from .base import BaseScan
from .full_scan import FullScan
from .single_collector import SingleCollector

all_scans = [SingleCollector, FullScan]

__all__ = ['BaseScan', 'all_scans']
