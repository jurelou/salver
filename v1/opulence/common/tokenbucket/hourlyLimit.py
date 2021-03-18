# -*- coding: utf-8 -*-
from .timeLimit import TimeLimit


class HourlyLimit(TimeLimit):
    def __init__(self, tokens, hours=1):
        self.tokens = tokens
        self.hours = hours * 3600

    def getTime(self):
        return self.hours
