import socket
import keyboard
import numpy as np


PORT = 5002

SERVER = '192.168.1.20'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
GET_DATA_MSG = bytes('1', encoding='utf8')
DISCONNECT_MSG = bytes('0', encoding='utf8')
SIZE = 2000000


def send(client):
    while True:
        if keyboard.is_pressed('\n'):
            while keyboard.is_pressed('\n'):
                pass
            client.send(GET_DATA_MSG)
            msg = ''
            response = client.recv(SIZE)
            msg += response.decode("utf-8")
            data = np.mat(msg)
            print(data)
        elif keyboard.is_pressed(' '):

            break

    client.send(DISCONNECT_MSG)

    client.close()


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('trying to connect...')
    client.connect(ADDR)
    print('CONNECTED!')
    send(client)
