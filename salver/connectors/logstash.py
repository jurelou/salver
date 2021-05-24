# -*- coding: utf-8 -*-
import json
import socket
import threading
from typing import List
import uuid
from loguru import logger

from salver.common import models
from salver.config import connectors_config
from salver.common.kafka import ConsumerCallback, Consumer


class LogstashClient:
    def __init__(self):
        self.host = connectors_config.logstash.host
        self.port = connectors_config.logstash.port

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

    def send_data(self, data):
        json_data = json.dumps(data).encode('utf-8') + b'\n'
        self.send(json_data)



class LogstashCallback(ConsumerCallback):
    def __init__(self):
        self.logstash_client = LogstashClient()

class OnCollectResponse(LogstashCallback):
    def on_message(self, collect_response: models.CollectResponse):
        logger.info(f'logstash connector: get collect result {collect_response}')

        data = {
            "scan_id": collect_response.scan_id.hex,
            "collect_id": collect_response.collect_id.hex,
            "@metadata": {
                'document_id': collect_response.fact.__hash__,
                'index': f"facts_{collect_response.fact.schema()['title'].lower()}",
            },
            **collect_response.fact.dict()
        }

        self.logstash_client.send_data(data)

class OnError(LogstashCallback):
    def on_message(self, error: models.Error):
        logger.info(f'logstash connector got error: {error.context}')
        data = error.dict()
        data["@metadata"] = {
                'index': "error",
                'document_id': uuid.uuid4().hex
        }
        self.logstash_client.send_data(data)

class OnScan(LogstashCallback):
    def on_message(self, scan: models.Scan):
        logger.info(f'logstash connector: got scan {scan.external_id}')
        for fact in scan.facts:
            data = {
                "scan_id": scan.external_id.hex,
                "@metadata": {
                    'document_id': fact.__hash__,
                    'index': f"facts_{fact.schema()['title'].lower()}",
                },
                **fact.dict()
            }

            self.logstash_client.send_data(data)

def make_consummers():
    common_params = {
        "num_workers": connectors_config.logstash.workers,
        "num_threads": connectors_config.logstash.threads,
        "schema_registry_url": connectors_config.kafka.schema_registry_url,
        "kafka_config": {
            'bootstrap.servers': connectors_config.kafka.bootstrap_servers,
            'group.id': "logstash-connector",
        },
    }
    return [
        Consumer(
                topic='collect-response',
                value_deserializer=models.CollectResponse,
                callback=OnCollectResponse,
                **common_params
        ),

        Consumer(
                topic='scan',
                value_deserializer=models.Scan,
                callback=OnScan,
                **common_params
        ),
        Consumer(
                topic='error',
                value_deserializer=models.Error,
                callback=OnError,
                **common_params
        ),
    ]
