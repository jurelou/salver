import socket
import json
from salver.facts import Person
from typing import List
from salver.common.models import BaseFact
import threading


p = Person(firstname="xx", lastname="ggggggg", bbbbbb="bbb")
p2 = Person(firstname="xx", lastname="ggggggggggggggggggggggg", bbbbbb="bbb")

class   LogstashInput:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
        self.lock = threading.Lock()
        self.socket = self.init_socket()

    def close(self):
        if self.socket:
            self.socket.close()

    def send(self, data):
        self.lock.acquire()
        try:
            print('sending data')
            self.socket.send(data)
        finally:
            self.lock.release()

    def init_socket(self):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print(f"Socket error {err}")
            return None
        try:
            sock.connect((self.host, self.port))
        except socket.error as err:
            print(f"Socket connect error {err}")
        return sock


    def send_facts(self, facts: List[BaseFact]):
        buffer = b""
        buf_size = 0
        for fact in facts:
            data = fact.dict(exclude={"hash__"})
            data["@metadata"] = {
                "document_id": fact.hash__,
                "fact_type": f"facts_{fact.schema()['title'].lower()}"
            }

            json_data = json.dumps(data).encode('utf-8')

            buffer = buffer + json_data + b"\n"
            buf_size = buf_size + len(json_data)

            if buf_size > 10000:
                self.send(buffer)
                buffer = ""
                buf_size = 0

        if buf_size != 0:
            self.send(buffer)

toto = LogstashInput("127.0.0.1", 5042)

toto.send_facts([p, p2])