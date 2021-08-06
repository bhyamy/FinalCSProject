import socket
import threading

SIZE = 1
PORT = 8080
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
REQUEST = '1'
DISCONNECT = '0'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    connected = True

    while connected:

        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == REQUEST:
            send_msg = 'WOOHOO'.encode(FORMAT)
            length = len(send_msg)
            send_length = str(length).encode(FORMAT)
            server.send(send_length)
            server.send(send_msg)
        elif msg == DISCONNECT:
            break

    conn.close()


if __name__ == '__main__':
    server.listen()
    print("listening...")
    conn, addr = server.accept()
    print("ACCEPTED!")
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

