# -*- coding: utf-8 -*-
from salver.common.utils import load_classes
from salver.common.models import BaseFact

all_facts = {
    mod.schema()["title"]: mod for mod in load_classes("salver/facts/", BaseFact)
}
