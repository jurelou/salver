# -*- coding: utf-8 -*-
from salver.common.exceptions import OpulenceException


class DatabaseException(OpulenceException):
    """Base engine exceptions."""

    def __init__(self, item):
        self.item = item


class ScanNotFound(DatabaseException):
    def __str__(self):
        return f"Scan {self.item} not found"


class CaseNotFound(DatabaseException):
    def __str__(self):
        return f"Case {self.item} not found"


class CaseAlreadyExists(DatabaseException):
    def __str__(self):
        return f"Case with name {self.item} already exists"
