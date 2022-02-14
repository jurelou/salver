# -*- coding: utf-8 -*-
import httpx
from loguru import logger
from salver.common.facts import Domain
from salver.agent.collectors import BaseCollector

class CertificateTransparency(BaseCollector):
    config = {
        'name': 'certificate-transparency',
    }

    def callbacks(self):
        return {Domain: self.from_domain}

    def from_domain(self, domain):
        res = httpx.get(f'https://crt.sh/?q=%.{domain.fqdn}&output=json', timeout=30)
        if res:
            for entry in res.json():
                logger.debug(entry)
                yield Domain(
                    fqdn=entry['common_name'],
                    certificate_issuer=entry['issuer_name'],
                    name_value=entry["name_value"],
                    serial_number=entry["serial_number"]
                )
        else:
            print(f'CT Error: {res}')