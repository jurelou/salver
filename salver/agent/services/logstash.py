# -*- coding: utf-8 -*-
import json
import socket
import threading
from typing import List

from loguru import logger

from salver.common.models import BaseFact
from salver.common.config import agent_config

class LogstashInput:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.lock = threading.Lock()
        self.socket = self.init_socket()

    def close(self):  # pragma: no cover
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def send(self, data):
        self.lock.acquire()
        try:
            self.socket.send(data)
        finally:
            self.lock.release()

    def init_socket(self):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:  # pragma: no cover
            logger.critical(f'Socket error: {err}')
            return None
        try:
            sock.connect((self.host, self.port))
        except socket.error as err:  # pragma: no cover
            logger.critical(f'Socket connect error: {err}')
        return sock

    def send_facts(self, facts: List[BaseFact]):
        buffer = b''
        batch_size = 0
        for fact in facts:
            data = fact.dict(exclude={'hash__'})
            data['@metadata'] = {
                'document_id': fact.hash__,
                'fact_type': f"facts_{fact.schema()['title'].lower()}",
            }
            logger.info(f'Push to logstash: {data}')

            json_data = json.dumps(data).encode('utf-8')

            buffer = buffer + json_data + b'\n'

            if batch_size >= engine_config.logstash.batch_size:
                self.send(buffer)
                buffer = b''
                batch_size = 0
            batch_size = batch_size + 1

        if buffer:
            self.send(buffer)
