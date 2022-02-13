import socket
from salver.agent.config import settings
from salver.common.facts import BaseFact

class LogstashClient:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((settings.logstash.ip, settings.logstash.port))
    
    def send_fact(self, fact: BaseFact):
        fact_str = fact.json() + "\n"
        print("ADD", fact_str)
        self.s.send(fact_str.encode())
