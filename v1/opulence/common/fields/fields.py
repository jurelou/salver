# -*- coding: utf-8 -*-
from .baseField import BaseField


class StringField(BaseField):
    def cast_value(self, value):
        return str(value)


class IntegerField(BaseField):
    def cast_value(self, value):
        return int(value)


class FloatField(BaseField):
    def cast_value(self, value):
        return float(value)


class BooleanField(BaseField):
    def cast_value(self, value):
        return bool(value)


class DynamicField(BaseField):
    pass
