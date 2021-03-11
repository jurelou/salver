from opulence.common.models.fact import BaseFact


class Phone(BaseFact):
    number: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"number": {"type": "keyword"}}}},
        )
