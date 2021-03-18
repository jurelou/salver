# -*- coding: utf-8 -*-
from .timeLimit import TimeLimit


class DailyLimit(TimeLimit):
    def __init__(self, tokens, days=1):
        self.tokens = tokens
        self.days = days * 3600 * 24

    def getTime(self):
        return self.days
