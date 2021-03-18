# -*- coding: utf-8 -*-
from opulence.common.exceptions import BaseOpulenceException


# Agents exceptions
class BaseAgentException(BaseOpulenceException):
    pass


class CollectorNotFound(BaseAgentException):
    pass


class CollectorDisabled(BaseAgentException):
    pass
