import httpx

from opulence.agent.collectors.base import BaseCollector
from opulence.facts.domain import Domain


class CertificateTransparency(BaseCollector):
    config = {
        "name": "certificate-transparency",
    }

    def callbacks(self):
        return {Domain: self.from_domain}

    def from_domain(self, domain):
        res = httpx.get(f"https://crt.sh/?q=%.{domain.fqdn}&output=json", timeout=30)
        if res:
            for entry in res.json():
                yield Domain(
                    fqdn=entry["common_name"], certificate_issuer=entry["issuer_name"]
                )
        else:
            print(f"CT Error: {res}")
