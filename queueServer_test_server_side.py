from Manager.DecisionMaker.queueServer import QueueServer
import threading

if __name__ == '__main__':
    queue = QueueServer(('localhost', 8080))
    thread = threading.Thread(target=queue.server_loop())
    thread.start()
