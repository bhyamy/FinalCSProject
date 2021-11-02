import time
from Manager.DecisionMaker.server import Server
import Manager.cnfigs as c
import queue
import logging


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
            msg = msg + ',' + name + ',' + str(value)
        # lose first comma
        if msg != '':
            msg = msg[1:]
            send_msg = msg.encode(c.FORMAT)
            """
            length = len(send_msg)
            send_length = str(length).encode(FORMAT)
            self.connection.send(send_length)
            """
            self.connection.send(send_msg)
        else:
            self.connection.send('-'.encode(c.FORMAT))

    def server_loop(self):
        """A loop that constantly runs until a disconnection request comes"""
        while True:
            try:
                msg = self.get_message()
                if msg == c.UNITY_REQUEST:
                    self.serve_client()
                elif msg == c.UNITY_DISCONNECT:
                    print("Unity client is disconnected.")
                    break
                elif msg != '':
                    print("Server loop error - Unity input is not handled.")
            except ConnectionError as e:
                print('Unity got disconnected')
                print('waiting for Unity to reconnect...')
                self.wait_for_client()
            except TimeoutError as e:
                print('Unity got disconnected')
                print('waiting for Unity to reconnect...')
                self.wait_for_client()
            except Exception as e:
                print('Server loop error')
                print(e.with_traceback(e.__traceback__))
            time.sleep(0)

    def put_in_queue(self, name, value):
        """Inserts tuple of strings to queue"""
        self.__update_queue.put((name, value))


'''
# for testing
elif msg == '2':
    self.put_in_queue('Dor', '0.5')
'''