from Manager.DecisionMaker.server import Server
from Manager.cnfigs import UNITY_REQUEST,UNITY_DISCONNECT
import queue


class QueueServer(Server):
    def __init__(self, address):
        super(address)
        self.__update_queue = queue.Queue()

    def serve_client(self):
        msg = ''
        while not self.server.empty():
            name, value = self.update_queue.get()
            msg = msg + ',' + name + ',' + value
        self.server.send(msg)

    def server_loop(self):
        while True:
            msg = self.get_message()
            if msg is UNITY_REQUEST:
                self.serve_client()
            elif msg is UNITY_DISCONNECT:
                print("Unity client is disconnected.")
                break
            elif msg is not '':
                print("error - Unity input is not handled.")

    def put_in_queue(self, name, value):
        self.update_queue.put((name, value))
