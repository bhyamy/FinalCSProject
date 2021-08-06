from Manager.DecisionMaker.server import Server
from Manager.cnfigs import UNITY_REQUEST, UNITY_DISCONNECT, FORMAT
import queue


class QueueServer(Server):
    """This is a class of a server with a FIFO queue.

    Attributes
    ----------
        __update_queue: Queue
            A queue for keeping tracks of required updates to client.

    Methods
    ----------
        serve_client()
            Empties update queue and sends the updates to the client as a concatenated string
            of 'name,value' updates.
        server_loop()
            A loop that constantly runs until a disconnection request comes
        put_in_queue(name, value)
            Inserts tuple of strings to queue.
    """

    def __init__(self, address):
        """

        Parameters
        ----------
            address: tuple
                A tuple of (ip, port)
        """
        super().__init__(address)
        self.__update_queue = queue.Queue()

    def serve_client(self):
        """Empties update queue and sends the updates to the client as a concatenated string
            of 'name,value' updates.
        """
        msg = ''
        while not self.__update_queue.empty():
            name, value = self.__update_queue.get()
            msg = msg + ',' + name + ',' + value
        # lose first comma
        msg = msg[1:]
        send_msg = msg.encode(FORMAT)
        length = len(send_msg)
        send_length = str(length).encode(FORMAT)
        self.connection.send(send_length)
        self.connection.send(send_msg)

    def server_loop(self):
        """A loop that constantly runs until a disconnection request comes"""
        while True:
            try:
                msg = self.get_message()
                if msg == UNITY_REQUEST:
                    self.serve_client()
                elif msg == UNITY_DISCONNECT:
                    print("Unity client is disconnected.")
                    break
                # for testing
                elif msg == '2':
                    self.put_in_queue('Dor', '0.5')
                elif msg != '':
                    print("error - Unity input is not handled.")
            except Exception as e:
                print(e.with_traceback(e.__traceback__))

    def put_in_queue(self, name, value):
        """Inserts tuple of strings to queue"""
        self.__update_queue.put((name, value))
