# -*- coding: utf-8 -*-
import time
<<<<<<< HEAD

from salver.config import connectors_config
from salver.connectors import mongodb, logstash

=======
from salver.config import connectors_config

from salver.connectors import mongodb
from salver.connectors import logstash
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

def make_consummers():
    consumers = []
    if connectors_config.mongo.enabled:
        consumers.extend(mongodb.make_consummers())

    if connectors_config.logstash.enabled:
        consumers.extend(logstash.make_consummers())
<<<<<<< HEAD

=======
        
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
    return consumers


if __name__ == '__main__':
    connectors = make_consummers()
    while True:
        for connector in connectors:
            connector.start_workers()
        time.sleep(5)
