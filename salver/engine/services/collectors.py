# -*- coding: utf-8 -*-
from salver.common.utils import load_classes
from salver.common.collectors import BaseCollector

all_collectors = load_classes(
    root_path='salver/agent/collectors',
    parent_class=BaseCollector,
)
