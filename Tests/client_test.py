import keyboard
import time

from Manager.DecisionMaker.client import Client
from Manager.cnfigs import UNITY_REQUEST, UNITY_DISCONNECT, UNITY_BUFFER_SIZE, UNITY_IP, UNITY_PORT, FORMAT

"""
A test for decisionMaker 
acts as unity client and asks for changes from decisionMaker server
"""
try:
    client = Client((UNITY_IP, UNITY_PORT))
    while True:
        if keyboard.is_pressed('\n'):
            while keyboard.is_pressed('\n'):
                pass
            break
        if keyboard.is_pressed('o'):
            while keyboard.is_pressed('o'):
                pass
            client.close_conn()
            exit(1)
        data = ''
        msg = bytes(UNITY_REQUEST, encoding='utf-8')
        client.client.send(msg)
        '''
        length = client.client.recv(UNITY_BUFFER_SIZE)
        length = length.decode(FORMAT)
        print(length)
        '''
        response = client.client.recv(UNITY_BUFFER_SIZE).decode(FORMAT)
        data += response
        if data != '-':
            print(data)
        time.sleep(0)

except Exception as e:
    print(e.with_traceback(e.__traceback__))

finally:
    time.sleep(1)
    msg = bytes(UNITY_DISCONNECT, encoding='utf-8')
    # time.sleep(5)
    client.send_msg(msg)
    client.close_conn()
    print('done')
