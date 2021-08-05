from abc import ABC, abstractmethod
from Manager.DecisionMaker.queueServer import QueueServer
from Manager.DecisionMaker.client import Client
import threading


class DecisionMaker(ABC):
    def __init__(self, processor, server_address, client_address):
        self.processor = processor
        self.__server = QueueServer(server_address)
        self.__server_thread = threading.Thread(self.server.server_loop())
        self.__server_thread.start()
        self.__eeg_client = Client(client_address)

    # will return a pairs list of game object names and their new values
    @abstractmethod
    def analyze(self, processed_data):
        pass

    def update(self, pairs_list):
        for name, value in pairs_list:
            self.server.put_in_queue(name, value)

    def take_decision(self):
        data = self.__eeg_client.get_eeg_data()
        processed_data = self.processor.process_data(data)
        pairs_list = self.analyze(processed_data)
        self.update(pairs_list)

    def is_unity_connected(self):
        return self.server_thread.is_alive()

    def disconnect_from_eeg(self):
            self.__eeg_client.disconnect_from_eeg()
