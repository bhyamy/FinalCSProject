import socket
import time

import Manager.cnfigs as c
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
        self.__client_address = address
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(c.EEG_CLIENT_TIMEOUT)
        self.connect_to_eeg()

    def connect_to_eeg(self):
        self.client.connect(self.__client_address)

    def disconnect_from_eeg(self):
        self.client.send(c.EEG_DISCONNECT_MSG.encode(c.FORMAT))
        time.sleep(1)
        self.client.close()

    def get_eeg_data(self):
        data = ''
        self.client.send(c.EEG_GET_DATA_MSG.encode(c.FORMAT))
        response = self.client.recv(c.EEG_BUFFER_SIZE)
        data += response.decode(c.FORMAT)
        if data == '':
            return []
        """
        print('data in client as string is:\n' + data)
        """
        data = np.mat(data)
        """
        print('data in client as string is:')
        print(data)
        """
        return data

    def send_msg(self, msg):
        self.client.send(msg)

    def close_conn(self):
        self.client.close()
