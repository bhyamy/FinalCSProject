from abc import ABC, abstractmethod
from Manager.Processor.processor import Processor
from Manager.DecisionMaker.queueServer import QueueServer
from Manager.cnfigs import UNITY_REQUEST, UNITY_DISCONNECT
import queue, threading


class DecisionMaker(ABC):
    def __init__(self, processor, address):
        self.processor = processor
        self.__server = QueueServer(address)
        self.__server_thread = threading.Thread(self.server.server_loop())
        self.__server_thread.start()

    # will return a pairs list of game object names and their new values
    @abstractmethod
    def analyze(self, processed_data):
        pass

    def update(self, pairs_list):
        for name, value in pairs_list:
            self.server.put_in_queue(name, value)

    def take_decision(self):
        processed_data = self.processor.get_processed_data()
        pairs_list = self.analyze(processed_data)
        self.update(pairs_list)

    def is_connected(self):
        return self.server_thread.is_alive()
