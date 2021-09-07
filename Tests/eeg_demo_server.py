"""
A demo server for unity update loop testing
"""
import socket
import threading
import time
import numpy as np

import keyboard
from Manager.cnfigs import EEG_DISCONNECT_MSG, EEG_GET_DATA_MSG, EEG_BUFFER_SIZE, EEG_IP, EEG_PORT, EEG_ELECTRODE_NUM,\
    EEG_SAMPLING_NUM, EEG_SAMPLING_RATE, FORMAT

SIZE = EEG_BUFFER_SIZE
PORT = EEG_PORT
SERVER = EEG_IP
FORMAT = FORMAT
REQUEST = EEG_GET_DATA_MSG
DISCONNECT = EEG_DISCONNECT_MSG


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handle_client(conn, addr):
    while True:
        try:
            msg = conn.recv(SIZE).decode(FORMAT)
            if msg == REQUEST:

                send_msg = str(np.random.rand(1, 71))
                send = send_msg.encode(FORMAT)
                conn.send(send)
            elif msg == DISCONNECT:
                break
        except Exception as e:
            print(e)
        time.sleep(0)
    conn.close()


if __name__ == '__main__':
    server.bind((SERVER, PORT))
    server.listen(1)
    print("listening...")
    con, add = server.accept()
    print("ACCEPTED!")
    thread = threading.Thread(target=handle_client, args=(con, add))
    thread.start()
    thread.join()
    print('done')

