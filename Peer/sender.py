from threading import Thread
import socket

class Sender(Thread):
    def __init__ (self, queue_sender, ips, my_ip, current_board, server_ip, socket):
        Thread.__init__(self)
        self.my_ip = my_ip
        self.port =  5001
        self.queue_sender = queue_sender
        self.ips = ips
        self.current_board = current_board
        self.server_ip = server_ip
        self.socket = socket

    def run(self):
        self.socket.pop()
        self.socket.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        send_current = 0
        remove_ip = ""

        while True:
            connected_to_first = True

            if len(self.ips) > 1:
                print("Sending data...")

                try:
                    next_index = self.ips.index(self.my_ip) + 1
                    if next_index < len(self.ips):
                        print("\tConnecting to the next on the network ring")
                        index = self.ips.index(self.my_ip) + 1
                        connected_to_first = False
                    else:
                        print("\tConnecting to the first IP of the network")
                        index = 0

                    print("\tTrying to connect to " + self.ips[index] + ":" + str(self.port) + "...")
                    self.socket[0].connect((self.ips[index], self.port))
                    print("\tSENDING DATA TO " + self.ips[index] + ":" + str(self.port))

                    if remove_ip != "":
                        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        msg = "remove " + remove_ip
                        print("\tUpdating '" + self.ips[index] + " with '" + msg + "'")
                        s_udp.sendto(msg.encode('utf-8'), (self.ips[index], 5002))
                        remove_ip = ""
                        s_udp.close()

                    while True:
                        if send_current < len(self.queue_sender):
                            self.socket[0].send(self.queue_sender[send_current].encode('utf-8'))
                            send_current = send_current + 1

                        next_index = self.ips.index(self.my_ip) + 1
                        if connected_to_first and next_index < len(self.ips):
                            print("\tStopping sending to the first, for send to the next in network")
                            self.socket[0].close()
                            self.socket.pop()
                            self.socket.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                            break

                except Exception as e:
                    self.socket[0].close()
                    remove_ip = self.ips[index]

                    self.socket.pop()
                    self.socket.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
                    msg_server = "remove " + remove_ip + " " + self.current_board
                    print("\tUpdating Server with '" + msg_server + "'")
                    self.socket[0].sendto(msg_server.encode('utf-8'), (self.server_ip, 6000))
                    self.socket[0].close()
                    
                    self.socket.pop()
                    self.socket.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                    self.ips.remove(self.ips[index])