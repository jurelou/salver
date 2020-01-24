import mongoengine


class Collector(mongoengine.DynamicDocument):
    meta = {"strict": False}

    external_identifier = mongoengine.StringField(primary_key=None)
