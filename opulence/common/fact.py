import hashlib
from time import time
from typing import Optional

from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator


class BaseFact(BaseModel):
    __hash: Optional[str] = None

    first_seen: float = Field(default_factory=time)
    last_seen: float = Field(default_factory=time)

    def __iter__(self):
        raise TypeError

    @root_validator
    def set_hash(cls, values):
        values.pop("hash__", None)
        m = hashlib.sha256()
        required_fields = cls.schema()["required"]

        for k in sorted(values):
            if k in required_fields:
                m.update(str(k).encode() + str(values[k]).encode())
        values["hash__"] = m.hexdigest()
        return values

    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "allow"

    @staticmethod
    def make_mapping(m):
        m["mappings"]["properties"]["first_seen"] = {"type": "float"}
        m["mappings"]["properties"]["last_seen"] = {"type": "float"}
        return m

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping({"mappings": {"properties": {}}})

    @staticmethod
    def from_obj(fact_type: str, data):
        from opulence.facts import all_facts  # pragma: nocover

        return all_facts[fact_type](**data)
