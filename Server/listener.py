from threading import Thread
from worker import Worker
import socket

class Listener(Thread):
    def __init__ (self, my_ip, my_port):
        Thread.__init__(self)
        self.my_ip = my_ip
        self.my_port =  my_port
        self.boards = {}

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.my_ip, self.my_port))

        while True:
            # Listen for messages UDP
            msg, client = s.recvfrom(65565)

            # Designates the message to Worker
            w = Worker(msg, client, self.boards)
            w.start()