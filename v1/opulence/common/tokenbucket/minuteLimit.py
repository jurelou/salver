# -*- coding: utf-8 -*-
from .timeLimit import TimeLimit


class MinuteLimit(TimeLimit):
    def __init__(self, tokens, minutes=1):
        self.tokens = tokens
        self.minutes = minutes * 60

    def getTime(self):
        return self.minutes
