# -*- coding: utf-8 -*-
import time

from salver.connectors import mongodb
from salver.config import connectors_config


def make_consummers():
    consumers = []
    if connectors_config.mongo.enabled:
        consumers.extend(mongodb.make_consummers())
    return consumers


if __name__ == '__main__':
    connectors = make_consummers()
    while True:
        for connector in connectors:
            connector.start_workers()
        time.sleep(5)