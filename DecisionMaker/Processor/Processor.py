import socket
from abc import ABC, abstractmethod
from cnfigs import EEG_DISCONNECT_MSG


class Processor(ABC):
    """
    An abstract class used to process incoming data.

    ...

    Attributes
    ----------
    client : socket
        a client to request real-time information from the EEG
    processed_data : None
        the data after it had been processed, type will be determined by implementing class

    Methods
    -------
    process()
        Process the real-time data
    get_processed_data()
        Returns the processed data
    connect(ip, port)
        Connects to socket
    disconnect()
        Disconnects from socket
    """
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(ip, port)
        self.processed_data = None

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
