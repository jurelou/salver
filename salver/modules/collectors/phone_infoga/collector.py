# -*- coding: utf-8 -*-
from salver.facts import Phone
from salver.common.utils import get_actual_dir
from salver.agent.collectors.docker import DockerCollector


class PhoneInfoga(DockerCollector):
    config = {
        "name": "phone-infoga",
        "docker": {"build_context": get_actual_dir()},
    }

    def callbacks(self):
        return {Phone: self.scan}

    def scan(self, phone):
        data = self.run_container(command=["scan", "-n", phone.number])

        for item in self.findall_regex(
            data,
            r"\[i\] Running local scan...\n\[\+\] Local format: (.*)\n\[\+\] \
            E164 format:.*\n\[\+\] International format: (.*)\n\[\+\] \
            Country found:.*\((.*)\)\n\[\+\] Carrier: (.*)",
        ):
            local_format, international_format, country_code, carrier = item

        for item in self.findall_regex(
            data,
            r"\[i\] Running Numverify.com scan...\n\[\+\] Valid: \
            (.*)\n\[\+\] Number:.*\n\[\+\] Local format: (.*)\n\[\+\] International format: \
            (.*)\n\[\+\] Country code: (.*) \(.*\n\[\+\] Country: (.*)\n\[\+\] Location: \
            (.*)\n\[\+\] Carrier: (.*)\n\[\+\] Line type: (.*)\n",
        ):
            (
                valid,
                nv_local_format,
                nv_international_format,
                nv_country_code,
                country,
                location,
                nv_carrier,
                line_type,
            ) = item

        local_format = local_format or nv_local_format
        international_format = international_format or nv_international_format
        country_code = country_code or nv_country_code
        carrier = carrier or nv_carrier

        yield Phone(
            number=phone.number,
            valid=valid,
            local_format=local_format,
            international_format=international_format,
            country_code=country_code,
            country=country,
            location=location,
            carrier=carrier,
            line_type=line_type,
        )
