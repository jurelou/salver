from opulence.common.fact import BaseFact


class Username(BaseFact):
    name: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"name": {"type": "keyword"},},},},
        )
