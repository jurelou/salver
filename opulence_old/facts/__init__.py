# -*- coding: utf-8 -*-
from opulence.facts.factory import FactFactory
from .company import Company
from .domain import Domain
from .email import Email
from .ipv4 import IPv4
from .ipv6 import IPv6
from .person import Person
from .phone import Phone
from .profile import Profile
from .socket import Socket
from .tweet import Tweet
from .uri import Uri
from .username import Username

all_facts = FactFactory().build()

__all__ = [
    "all_facts",
    "Company",
    "Domain",
    "Email",
    "IPv4",
    "IPv6",
    "Person",
    "Phone",
    "Profile",
    "Socket",
    "Tweet",
    "Uri",
    "Username",
]
