import socket
from Manager.cnfigs import EEG_DISCONNECT_MSG, EEG_GET_DATA_MSG, EEG_BUFFER_SIZE, FORMAT


class Client(object):
    def __init__(self, address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_eeg(address)

    def connect_to_eeg(self, client_address):
            self.client.connect(client_address)

    def disconnect_from_eeg(self):
            self.client.send(EEG_DISCONNECT_MSG)
            self.client.close()

    def get_eeg_data(self):
        data = ''
        self.client.send(EEG_GET_DATA_MSG)
        response = self.client.recv(EEG_BUFFER_SIZE)
        data += response.decode(FORMAT)
        return data
