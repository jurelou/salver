from opulence.common.fact import BaseFact


class Account(BaseFact):
    address: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"address": {"type": "keyword"}}}},
        )
