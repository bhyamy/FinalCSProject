from abc import ABC, abstractmethod
from Processor import Processor


class DecisionMaker(ABC):

    @abstractmethod
    def take_decision(self):
        pass
