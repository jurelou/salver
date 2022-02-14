import socket
import ujson
import errno
import time
from loguru import logger

from salver.agent.config import settings
from salver.common.facts import BaseFact

class LogstashClient:
    def __init__(self):
        self.s = None
        self.connect()
    
    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:  # pragma: no cover
            logger.critical(f'Socket error: {err}')
            return
        try:
            self.s.connect((settings.logstash.ip, settings.logstash.port))
        except socket.error as err:
            logger.critical(f'Socket connect error: {err}')

    def send(self, data):
        try:
            self.s.send(data)
        except IOError as err:
            if err.errno == errno.EPIPE:
                logger.critical("Could not connect to logstash, retrying")
                time.sleep(1)
                self.connect()
                self.send(data)

    def send_fact(self, source: str, scan_id, fact: BaseFact):
        fact_type = fact.schema()["title"]
        fact_dict = {
            "@metadata": {
                "index": f"facts-{fact_type.lower()}",
            },
            "fact_type": fact_type,
            "fact_source": source,
            "scan_id": scan_id,
            **fact.dict()
        }
        fact_str = ujson.dumps(fact_dict).encode('utf-8') + b"\n"
        self.send(fact_str)
