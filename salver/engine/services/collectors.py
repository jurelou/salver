from salver.common.collectors import BaseCollector
from salver.common.utils import load_classes

all_collectors = load_classes(
        root_path='salver/agent/collectors',
        parent_class=BaseCollector,
)