from abc import ABC, abstractmethod

class Processor(ABC):
    def __init__(self):
        self.processed_data = None

    @abstractmethod
    def process(self, data):
        pass

    def process_data(self, data):
        self.process(data)
        return self.processed_data

