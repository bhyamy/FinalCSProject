import time
from abc import ABC, abstractmethod
from Manager.DecisionMaker.queueServer import QueueServer
from Manager.DecisionMaker.client import Client
import threading


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
        print('connected to EEG.')
        self.__server = QueueServer(server_address)
        self.last_decision_time = time.localtime(time.time())
        self.__server_thread = threading.Thread(target=self.__server.server_loop)
        self.__server_thread.start()

    @abstractmethod
    def analyze(self, processed_data):
        pass

    def update(self, pairs_list):
        """Updates to __server the desired updates"""
        for name, value in pairs_list:
            self.__server.put_in_queue(name, value)

    def take_decision(self):
        """Takes decisions based on processed data and analyzing it"""
        pairs_list = []
        try:
            data = self.__eeg_client.get_eeg_data()
            eeg_status = 'eeg_connected', 1
            processed_data = self.processor.process_data(data)
            pairs_list = self.analyze(processed_data)
        except ValueError as e:
            eeg_status = 'eeg_connected', 0
            print('take decision Value error')
            print(e.with_traceback(e.__traceback__))
        except ConnectionError as e:
            eeg_status = 'eeg_connected', 0
            print('eeg got disconnected.')
            print('trying to reconnect...')
            self.__eeg_client.connect_to_eeg()
        except Exception as e:
            eeg_status = 'eeg_connected', 0
            print('take decision General error')
            print(e.with_traceback(e.__traceback__))
        finally:
            pairs_list.append(eeg_status)
            self.update(pairs_list)
            time.sleep(0)

    def is_unity_connected(self):
        """Checks if VR client is connected"""
        return self.__server_thread.is_alive()

    def disconnect_from_eeg(self):
        """Disconnects from socket"""
        self.__eeg_client.disconnect_from_eeg()

    def wait_for_server(self):
        self.__server_thread.join()
