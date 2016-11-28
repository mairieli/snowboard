from threading import Thread
from worker import Worker
import socket

class Listener(Thread):
    def __init__ (self, host, port):
        Thread.__init__(self)
        self.host = host
        self.port =  port
        self.table = {}

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))

        while True:
            msg, client = s.recvfrom(65565)
            w = Worker(msg, client, self.table)
            w.start()