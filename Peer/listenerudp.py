from threading import Thread
import socket

class Listener_UDP(Thread):
    def __init__ (self, ips, my_ip):
        Thread.__init__(self)
        self.host = ''
        self.port =  5002
        self.ips = ips
        self.my_ip = my_ip

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))
        print("Waiting for UDP on " + self.my_ip + ":" + str(self.port))

        while True:
            msg, client = s.recvfrom(65565)
            msg = msg.decode('utf-8')
            print("Received '" + msg + "' from " + client[0] + ":" + str(client[1]))
            if msg.startswith("connect"):
                print(client[0] + " is the last Peer now")
                self.ips.append(client[0])
            elif msg.startswith("remove"):
                removed_ip = msg.split(" ")[1]
                print(removed_ip + " is no longer in network")
                self.ips.remove(removed_ip)