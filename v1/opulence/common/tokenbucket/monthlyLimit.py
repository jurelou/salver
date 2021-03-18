# -*- coding: utf-8 -*-
from .timeLimit import TimeLimit


class MonthlyLimit(TimeLimit):
    def __init__(self, tokens, months=1):
        self.tokens = tokens
        self.months = months * 3600 * 24 * 31

    def getTime(self):
        return self.months
