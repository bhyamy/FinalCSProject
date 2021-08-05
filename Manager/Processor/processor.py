from abc import ABC, abstractmethod


class Processor(ABC):
    """
    An abstract class used to process incoming data.

    ...

    Attributes
    ----------
    processed_data : None
        the data after it had been processed, type will be determined by implementing class

    Methods
    -------
    process()
        Process the real-time data
    get_processed_data()
        Returns the processed data
    """
    def __init__(self):
        self.processed_data = None

    @abstractmethod
    def process(self, data):
        pass

    def process_data(self, data):
        self.process(data)
        return self.processed_data

