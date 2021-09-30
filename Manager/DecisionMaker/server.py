import socket
from singletons import Config


class Server(object):
    """Class of a server.

    Attributes:
    ----------
        server: socket
            Communication socket with Unity client
        connection: socket
            Connection socket to interact with Unity client
    Methods:
    ----------
        send(msg)
            Send message to client
        close_connection()
            Close connection with client
        get_message()
            Get the message message from client
    """
    def __init__(self, address):
        """
        Parameters:
            address: tuple
                Tuple of (ip, port)
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(address)
        self.server.listen(1)
        print("listening...")
        self.connection, _ = self.server.accept()
        print("ACCEPTED!")
        confs = Config()
        self.format = confs.configs['FORMAT']
        self.buffer_size = confs.configs['UNITY']['BUFFER_SIZE']

    def send(self, msg):
        """Send message to client"""
        self.server.send(msg)

    def close_connection(self):
        """Close connection with client"""
        self.connection.close()

    def get_message(self):
        """Get the message message from client"""
        return self.connection.recv(self.buffer_size).decode(self.format)
