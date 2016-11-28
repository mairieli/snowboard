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

            ip = msg.split(" ")[1]
            if msg.startswith("connect"):
                print(ip + " is the last Peer now")
                self.ips.append(ip)
            elif msg.startswith("remove"):
                ip = msg.split(" ")[1]
                print(ip + " is no longer in network")
                self.ips.remove(ip)
            next_index = self.ips.index(self.my_ip) + 1
            if next_index < len(self.ips):
                index = next_index
            else:
                index = 0
            s.socket.sendto(msg.encode('utf-8'), (self.ips[index], 5002))
