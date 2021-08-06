import socket
import keyboard


PORT = 8080
SERVER = 'localhost'
ADDR = (SERVER, PORT)
GET_DATA_MSG = bytes('1', encoding='utf-8')
DISCONNECT_MSG = bytes('0', encoding='utf-8')
PUT_IN_QUEUE = bytes('2', encoding='utf-8')
SIZE = 2000


def test(client):
    while True:
        if keyboard.is_pressed('\n'):
            while keyboard.is_pressed('\n'):
                pass
            client.send(GET_DATA_MSG)
            msg = ''
            response = client.recv(SIZE)
            msg += response.decode("utf-8")
            print(msg)
        elif keyboard.is_pressed('2'):
            while keyboard.is_pressed('2'):
                pass
            client.send(PUT_IN_QUEUE)
        elif keyboard.is_pressed(' '):
            client.send(DISCONNECT_MSG)
            break

    client.send(DISCONNECT_MSG)
    print("Closed")
    client.close()


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('trying to connect...')
    client.connect(ADDR)
    print('CONNECTED!')
    test(client)
