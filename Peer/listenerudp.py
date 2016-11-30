from threading import Thread
import socket

class Listener_UDP(Thread):
    def __init__ (self, ips, my_ip, my_board, host_ip):
        Thread.__init__(self)
        self.host = ''
        self.port =  5002
        self.ips = ips
        self.my_ip = my_ip
        self.my_board = my_board
        self.host_ip = host_ip

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
                if ip in self.ips:
                    continue
                print(ip + " is the last Peer now")
                self.ips.append(ip)
            elif msg.startswith("remove"):
                if ip not in self.ips:
                    continue
                ip = msg.split(" ")[1]
                print(ip + " is no longer in network")
                msg_server = "remove " + ip + " " + self.my_board
                s.sendto(msg_server.encode('utf-8'), (self.host_ip, 6000))
                self.ips.remove(ip)
            print("Updated IPs", end=" ")
            print(self.ips)
            next_index = self.ips.index(self.my_ip) + 1
            if next_index < len(self.ips):
                index = next_index
            else:
                index = 0
            s.sendto(msg.encode('utf-8'), (self.ips[index], 5002))