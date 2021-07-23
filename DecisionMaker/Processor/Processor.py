import socket
from abc import ABC, abstractmethod
from cnfigs import EEG_DISCONNECT_MSG


class Processor(ABC):
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.processed_data = None
        self.connect(ip, port)

    @abstractmethod
    def process(self):
        pass

    def get_processed_data(self):
        self.process()
        return self.processed_data

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def disconnect(self):
        self.client.send(EEG_DISCONNECT_MSG)
        self.client.close()
