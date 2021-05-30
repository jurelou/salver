<<<<<<< HEAD
# -*- coding: utf-8 -*-
from salver.common.utils import load_classes
from salver.common.collectors import BaseCollector

all_collectors = load_classes(
    root_path='salver/agent/collectors',
    parent_class=BaseCollector,
)
=======
from salver.common.collectors import BaseCollector
from salver.common.utils import load_classes

all_collectors = load_classes(
        root_path='salver/agent/collectors',
        parent_class=BaseCollector,
)
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
