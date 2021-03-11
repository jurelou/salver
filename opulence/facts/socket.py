from opulence.common.fact import BaseFact


class Socket(BaseFact):
    port: int
    proto: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {
                "mappings": {
                    "properties": {
                        "port": {"type": "integer"},
                        "proto": {"type": "keyword"},
                    }
                }
            },
        )
