import ipaddress

from pydantic import validator

from opulence.common.fact import BaseFact


class IPv4(BaseFact):
    address: str

    @validator("address")
    def check_valid_ipv4(cls, v):
        try:
            ipaddress.IPv4Address(v)
        except ipaddress.AddressValueError as err:
            raise ValueError(f"Fact IPv4 is invalid: {err}")
        return v

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"address": {"type": "ip"}}}},
        )
