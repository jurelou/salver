# -*- coding: utf-8 -*-
from salver.facts import Email, Username
from salver.common.limiter import Duration, RequestRate
from salver.agent.collectors.base import BaseCollector


class Dummy(BaseCollector):
    config = {
        'name': 'dummy-collector',
        'limiter': [RequestRate(limit=1, interval=Duration.SECOND)],
    }

    def callbacks(self):
        return {
            Email: self.cb_email,
        }

    def cb_email(self, email):
        yield Username(name=f'Mr. {email.address}')
        yield Username(name=f'Mrs. {email.address}')
