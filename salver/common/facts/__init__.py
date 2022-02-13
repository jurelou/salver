# -*- coding: utf-8 -*-
from .base import BaseFact
from .factory import FactFactory
from .personnal.email import Email
from .personnal.person import Person
from .personnal.username import Username

all_facts = FactFactory().build()

__all__ = ["BaseFact", "all_facts", "Email", "Person", "Username"]
