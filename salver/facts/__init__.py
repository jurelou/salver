# -*- coding: utf-8 -*-
from salver.facts.factory import FactFactory
from salver.facts.modules import *  # noqa: F403,F401

all_facts = FactFactory().build()

__all__ = ['all_facts']
