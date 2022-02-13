# -*- coding: utf-8 -*-
from .base import BaseFact
from .factory import FactFactory

from .personnal.email import Email
from .personnal.person import Person
from .personnal.username import Username
from .personnal.online_profile import OnlineProfile

from .infrastructure.domain import Domain
from .infrastructure.ipv4 import IPv4

from .others.company import Company


all_facts = FactFactory().build()

__all__ = [
    "BaseFact",
    "all_facts",
    "Email",
    "Person",
    "Username",
    "OnlineProfile",
    "Company",
    "Domain"
]
