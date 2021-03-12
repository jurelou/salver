import ipaddress

from pydantic import validator

from opulence.common.models.fact import BaseFact


class IPv6(BaseFact):
    address: str

    @validator("address")
    def check_valid_ipv4(cls, v):
        try:
            ipaddress.IPv6Address(v)
        except ipaddress.AddressValueError as err:
            raise ValueError(f"Fact IPv6 is invalid: {err}")
        return v

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"address": {"type": "ip"}}}},
        )
