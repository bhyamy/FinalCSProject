import socket
import threading
from Manager.cnfigs import FORMAT, UNITY_IP, UNITY_PORT, UNITY_BUFFER_SIZE, UNITY_REQUEST, UNITY_DISCONNECT


class MyServer(object):
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


def main():
    server = MyServer((UNITY_IP, UNITY_PORT))

    connected = True

    while connected:

        msg = server.get_message()
        if msg == UNITY_REQUEST:
            pass
        elif msg == UNITY_DISCONNECT:
            break

    server.close_connection()


if __name__ == '__main__':
    main()
