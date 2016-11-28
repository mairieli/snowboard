from threading import Thread
import socket

class Listener_UDP(Thread):
    def __init__ (self, ips):
        Thread.__init__(self)
        self.host = ''
        self.port =  5002
        self.ips = ips

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))

        while True:
            msg, client = s.recvfrom(65565)
            msg = msg.decode('utf-8')
            if msg.startswith("connect"):
                self.ips.append(client[0])
            elif msg.startswith("remove"):
                msg = msg.split(" ")
                self.ips.remove(msg[1])