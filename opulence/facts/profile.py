from opulence.common.fact import BaseFact


class Profile(BaseFact):
    url: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"url": {"type": "keyword"}}}},
        )
