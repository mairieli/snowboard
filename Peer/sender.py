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
        remove_ip = ""

        while True:
            connected_to_first = False

            if len(self.ips) > 1:
                print("Sending data...")

                try:
                    my_ip = socket.gethostbyname(socket.gethostname())
                    if self.ips.index(my_ip) + 1:
                        print("Connecting to the next on the network")
                        index = self.ips.index(my_ip) + 1
                    else:
                        print("Connecting to the first IP of the network")
                        index = self.ips[0]
                        connected_to_first = True

                    print("Trying to connect to " + self.ips[index] + ":" + str(self.port))
                    s.connect((self.ips[index], self.port))
                    print("Sending data to " + self.ips[index] + ":" + str(self.port))

                    if remove_ip != "":
                        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        msg = "remove " + remove_ip
                        print("Sending UDP '" + msg + "' to " + self.ips[index] + ":5002")
                        s_udp.sendto(msg.encode('utf-8'), (self.ips[index], 5002))
                        remove_ip = ""

                    while True:
                        if send_current < len(self.queue_sender):
                            s.send(self.queue_sender[send_current].encode('utf-8'))
                            send_current = send_current + 1
                        if connected_to_first and self.ips[self.ips.index(my_ip) + 1]:
                            print("Stopping sending to the first, for send to the next")
                            break

                except Exception as e:
                    print(e.args)
                    remove_ip = self.ips.pop()