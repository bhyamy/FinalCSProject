import socket
import time
from singletons import Config
import numpy as np


class Client(object):
    """
    This is a client class for custom communication with the EEG server.

    ...

    Attributes
    ----------
    client : socket
        a client to request real-time information from the EEG

    Methods
    -------
    connect_to_eeg(address)
        Connects to the server on the EEG computer.
    disconnect_from_eeg()
        Disconnects from server.
    get_eeg_data()
        Sends request to server and returns real time samples from EEG+GSR
        (matrix of size samples X channels[64+7=71])
    """
    def __init__(self, address):
        confs = Config()
        self.format = confs.configs['FORMAT']
        self.disconnect_msg = confs.configs['EEG']['DISCONNECT']
        self.buffer_size = confs.configs['EEG']['BUFFER_SIZE']
        self.get_data_msg = confs.configs['EEG']['REQUEST']
        self.__client_address = address
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(confs['EEG']['EEG_CLIENT_TIMEOUT'])
        self.connect_to_eeg()

    def connect_to_eeg(self):
        self.client.connect(self.__client_address)

    def disconnect_from_eeg(self):
        self.client.send(self.disconnect_msg.encode(self.format))
        time.sleep(1)
        self.client.close()

    def get_eeg_data(self):
        data = ''
        self.client.send(self.get_data_msg.encode(self.format))
        response = self.client.recv(self.buffer_size)
        data += response.decode(self.format)
        if data == '':
            return []
        data = np.mat(data)

        return data

    def send_msg(self, msg):
        self.client.send(msg)

    def close_conn(self):
        self.client.close()
