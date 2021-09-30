import socket
import time
import numpy as np
from singletons import Config


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
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_eeg(address)
        confs = Config()
        self.format = confs.configs['FORMAT']
        self.disconnect_msg = confs.configs['EEG']['DISCONNECT']
        self.buffer_size = confs.configs['EEG']['BUFFER_SIZE']
        self.get_data_msg = confs.configs['EEG']['REQUEST']

    def connect_to_eeg(self, client_address):
        self.client.connect(client_address)

    def disconnect_from_eeg(self):
        self.client.send(EEG_DISCONNECT_MSG.encode(FORMAT))
        time.sleep(1)
        self.client.close()

    def get_eeg_data(self):
        data = ''
        self.client.send(EEG_GET_DATA_MSG.encode(FORMAT))
        response = self.client.recv(EEG_BUFFER_SIZE)
        data += response.decode(FORMAT)
        if data == '':
            return []
        data = np.mat(data)
        return data

    def send_msg(self, msg):
        self.client.send(msg)

    def close_conn(self):
        self.client.close()
