# -*- coding: utf-8 -*-
import mongoengine

from opulence.common.utils import now


class Result(mongoengine.DynamicDocument):
    meta = {"strict": False}

    result_identifier = mongoengine.StringField()


class Collector_result(mongoengine.DynamicDocument):
    meta = {"strict": False}

    identifier = mongoengine.StringField(primary_key=True)
    scan_identifier = mongoengine.StringField()


class Stats(mongoengine.EmbeddedDocument):
    start_date = mongoengine.ComplexDateTimeField(default=now)
    end_date = mongoengine.ComplexDateTimeField()
    number_of_results = mongoengine.IntField(default=0)


class Scan(mongoengine.DynamicDocument):
    meta = {"strict": False}
    external_identifier = mongoengine.StringField(primary_key=True)
    stats = mongoengine.EmbeddedDocumentField(Stats)
    scan_type = mongoengine.StringField(default="Unknown")
