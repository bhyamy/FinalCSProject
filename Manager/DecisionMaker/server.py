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
        self.connection = None
        self.wait_for_client()
        confs = Config()
        self.format = confs.configs['FORMAT']
        self.buffer_size = confs.configs['UNITY']['BUFFER_SIZE']
        self.conn_timeout = confs.configs['UNITY']['CLIENT_TIMEOUT']
        self.msg_timeout = confs.configs['UNITY']['MESSAGE_TIMEOUT']

    def wait_for_client(self):
        self.server.listen(1)
        print("listening...")
        self.server.settimeout(self.conn_timeout)
        self.connection, _ = self.server.accept()
        print("ACCEPTED!")
        self.connection.settimeout(self.msg_timeout)

    def send(self, msg):
        """Send message to client"""
        self.server.send(msg)

    def close_connection(self):
        """Close connection with client"""
        self.connection.close()

    def get_message(self):
        """Get the message message from client"""
        return self.connection.recv(self.buffer_size).decode(self.format)
