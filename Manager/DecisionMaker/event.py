from abc import ABC, abstractmethod
from Manager.cnfigs import EEG_SAMPLING_RATE

class Event(ABC):
    def __init__(self, str):
        range, threshold, name, value = self.__parse_string(str)
        self.__range = range
        self.__threshold = threshold
        self.__name = name
        self.__value = value

    # checking if csv row values are valid
    def __parse_string(self, str):
        min_range = float(str[0])
        max_range = float(str[1])
        threshold = float(str[2])
        name = str[3]
        value = str[4]
        return (min_range,max_range), threshold, name, value

    def should_be_activated(self, processed_data):
        for i in range(self.__range[0]*EEG_SAMPLING_RATE, self.__range[1]*EEG_SAMPLING_RATE+1):
            if processed_data[i] > self.__threshold: return True
        return False

    def get_change(self):
        return (self.__name, self.__value)
