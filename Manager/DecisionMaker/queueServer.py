from Manager.DecisionMaker.server import Server
from Manager.cnfigs import UNITY_REQUEST,UNITY_DISCONNECT
import queue


class QueueServer(Server):
    """
    This is a server class that also contains and update queue.

    An object of this class contains a FIFO queue of tuples (name [of speaker], value [change volume])
    that say what needs to happen.

    Attributes
    ----------
    __update_queue: queue
        Queue of updates to VR scene.

    Methods
    ----------
        serve_client()
            Sends a message of concatenated updates to Unity client.
        server_loop()
            Loop that checks if a request came from the client and handles it.
        put_in_queue(name, value)
            Puts in the queue a tuple of (name, value)
    """
    def __init__(self, address):
        """
        Parameters:
            address: tuple
                Tuple of (ip, port)
        """
        super().__init__(address)
        self.__update_queue = queue.Queue()

    def serve_client(self):
        """Sends a message of concatenated updates to Unity client"""
        msg = ''
        while not self.__update_queue.empty():
            name, value = self.__update_queue.get()
            msg = msg + ',' + name + ',' + value
        # lose first comma
        msg = msg[1:]
        self.server.send(msg)

    def server_loop(self):
        """Checks if a request came from the client and handles it"""
        while True:
            msg = self.get_message()
            if msg is UNITY_REQUEST:
                self.serve_client()
            elif msg is UNITY_DISCONNECT:
                self.server.close_connection()
                print("Unity client is disconnected.")
                break
            elif msg is not '':
                print("error - Unity input is not handled.")

    def put_in_queue(self, name, value):
        """Puts in the queue a tuple of (name, value).

        Parameters:
        ----------
            name: str
                Name of speaker.
            value: str
                How to change speakers audio (string representation of float).
        """
        self.update_queue.put((name, value))
