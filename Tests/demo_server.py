"""
A demo server for unity update loop testing
"""
import socket
import threading
import keyboard

SIZE = 1024
PORT = 5001
SERVER = 'localhost'
FORMAT = 'utf-8'
REQUEST = '1'
DISCONNECT = '0'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handle_client(conn, addr):
    while True:
        try:
            msg = conn.recv(SIZE).decode(FORMAT)
            if msg == REQUEST:
                if keyboard.is_pressed('\n'):
                    while keyboard.is_pressed('\n'):
                        pass
                    send_msg = 'sound_source_1,1,sound_source_2,0,Light_source_1,1,Light_source_2,0'
                elif keyboard.is_pressed(' '):
                    while keyboard.is_pressed(' '):
                        pass
                    send_msg = 'sound_source_1,0,sound_source_2,1,Light_source_1,0,Light_source_2,1'
                elif keyboard.is_pressed('a'):
                    while keyboard.is_pressed('a'):
                        pass
                    send_msg = 'sound_source_1,1,sound_source_2,1,Light_source_1,1,Light_source_2,1'
                elif keyboard.is_pressed('n'):
                    while keyboard.is_pressed(' '):
                        pass
                    send_msg = 'sound_source_1,0,sound_source_2,0,Light_source_1,0,Light_source_2,0'
                else:
                    send_msg = '-'
                """
                length = len(send_msg)
                send_length = str(length).encode(FORMAT)
                conn.send(send_length)
                """
                send = send_msg.encode(FORMAT)
                conn.send(send)
            elif msg == DISCONNECT:
                print('client disconnected')
                break
        except Exception as e:
            print(e)
    print('closing server...')
    conn.close()
    print('server is closed!')


if __name__ == '__main__':
    server.bind((SERVER, PORT))
    server.listen(1)
    print("listening...")
    conn, addr = server.accept()
    print("ACCEPTED!")
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

