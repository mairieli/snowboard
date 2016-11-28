from threading import Thread
import socket

class Sender(Thread):
    def __init__ (self, queue_sender, ips):
        Thread.__init__(self)
        self.port =  5001
        self.queue_sender = queue_sender
        self.ips = ips

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_current = 0
        removed_ip = ""
        while True:
            first = False
            if len(self.ips) > 0:
                try:
                    my_ip = socket.gethostbyname(socket.gethostname())
                    if self.ips.index(my_ip) + 1:
                        index = self.ips.index(my_ip) + 1
                    else:
                        index = self.ips[0]
                        fist = True
                    s.connect((self.ips[index], self.port))
                    if removed_ip != "":
                        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        response = "remove " + removed_ip
                        udp.sendto(response.encode('utf-8'), (self.ips[index], 5002))
                        removed_ip = ""
                    while True:
                        if send_current < len(self.queue_sender)
                            s.send(queue_sender[send_current])
                            send_current = send_current + 1
                        if first and self.ips[self.ips.index(my_ip) + 1]:
                            break
                catch:
                    removed_ip = self.ips.pop()