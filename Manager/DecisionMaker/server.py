import socket
from Manager.cnfigs import FORMAT, UNITY_BUFFER_SIZE
import threading


class Server(object):
    def __init__(self, address):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(address)
        self.server.listen()
        self.connection, _ = self.server.accept()

    def send(self, msg):
        self.server.send(msg)

    def close_connection(self):
        self.connection.close()

    def get_message(self):
        return self.connection.recv(UNITY_BUFFER_SIZE).decode(FORMAT)