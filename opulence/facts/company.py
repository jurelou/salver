from opulence.common.models.fact import BaseFact


class Company(BaseFact):
    name: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"name": {"type": "keyword"}}}},
        )
