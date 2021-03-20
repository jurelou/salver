# -*- coding: utf-8 -*-
from opulence.agent.collectors.base import BaseCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.email import Email
from opulence.facts.username import Username


class Dummy(BaseCollector):
    config = {
        "name": "dummy-collector",
    }

    def callbacks(self):
        return {
            Email: self.cb_email,
        }

    def cb_email(self, email):
        yield Username(name=f"Mr. {email.address}")
