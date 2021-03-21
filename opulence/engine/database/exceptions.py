# -*- coding: utf-8 -*-
from opulence.engine.exceptions import EngineException


class DatabaseException(EngineException):
    """Base engine exceptions."""

    def __init__(self, item):
        self.item = item


class ScanNotFound(DatabaseException):
    def __str__(self):
        return f"Scan {self.item} not found"


class CaseNotFound(DatabaseException):
    def __str__(self):
        return f"Case {self.item} not found"
