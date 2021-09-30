from abc import ABC, abstractmethod
from Manager.DecisionMaker.queueServer import QueueServer
from Manager.DecisionMaker.client import Client
import threading
import datetime
from time import perf_counter
from singletons import Logger


class DecisionMaker(ABC):
    """A base abstract class for decision making based on real time data.

    Attributes
    ----------
        processor: Processor
            Processor of the data.
        __server: QueueServer
            Server that communicates with the VR Client
        __server_thread: thread
            Communication thread
        __eeg_client: socket
            Socket for communication with the EEG client
        
    Methods
    ----------
        analyze(processed_data)
            Abstract method to analyze the data
        update(pairs_list)
            Updates to __server the desired updates
        take_decision()
            Takes decisions based on processed data and analyzing it
        is_unity_connected()
            Checks if VR client is connected
        disconnect_from_eeg()
            Disconnects from socket
    """
    def __init__(self, processor, server_address, client_address):
        self.processor = processor
        self.__eeg_client = Client(client_address)
        self.__server = QueueServer(server_address)
        self.__server_thread = threading.Thread(target=self.__server.server_loop)
        self.__server_thread.start()
        self.logger = Logger()

    @abstractmethod
    def analyze(self, processed_data):
        pass

    def update(self, pairs_list):
        """Updates to __server the desired updates"""
        for name, value in pairs_list:
            self.__server.put_in_queue(name, value)

    def take_decision(self):
        """Takes decisions based on processed data and analyzing it"""
        try:
            # TODO - ask Yair about how much verbosity is needed!
            # get data from server
            start_time = perf_counter()
            self.logger.print(f'Get Data Request sent at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            data = self.__eeg_client.get_eeg_data()
            end_time = perf_counter()

            self.logger.print(f'Data Received at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            self.logger.print(f'Data is:\n {data}')
            self.logger.print(f'Time elapsed in seconds: {start_time - end_time}')
            self.logger.print(
                f'Processing and analyzing started at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

            # process and analyze data
            start_time = perf_counter()

            processed_data = self.processor.process_data(data)
            pairs_list = self.analyze(processed_data)

            end_time = perf_counter()

            self.logger.print(
                f'Processing and analyzing finished at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            self.logger.print(f'Time elapsed in seconds: {start_time - end_time}')

            self.logger.add_to_buffer(str(data))
            self.logger.add_to_buffer(str(pairs_list))

            self.update(pairs_list)
        except ValueError as e:
            print('Value error')
            print(e.with_traceback(e.__traceback__))
        except Exception as e:
            print(e.with_traceback(e.__traceback__))

    def is_unity_connected(self):
        """Checks if VR client is connected"""
        return self.__server_thread.is_alive()

    def disconnect_from_eeg(self):
        """Disconnects from socket"""
        self.__eeg_client.disconnect_from_eeg()

    def wait_for_server(self):
        self.__server_thread.join()
