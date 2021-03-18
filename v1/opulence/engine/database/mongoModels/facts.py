# -*- coding: utf-8 -*-
import mongoengine


class Fact(mongoengine.DynamicDocument):
    meta = {"strict": False}

    external_identifier = mongoengine.StringField(primary_key=None)
