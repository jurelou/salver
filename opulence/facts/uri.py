from opulence.common.fact import BaseFact


class Uri(BaseFact):
    location: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"location": {"type": "keyword"}}}},
        )