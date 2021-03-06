from threading import Thread
import socket

class Listener(Thread):
    def __init__ (self, my_color, queue_receiver, queue_sender, ips, my_ip, socket):
        Thread.__init__(self)
        self.my_ip = my_ip
        self.port =  5001
        self.queue_receiver = queue_receiver
        self.queue_sender = queue_sender
        self.my_color = my_color
        self.ips = ips
        self.socket = socket

    def run(self):
        self.socket.pop()
        self.socket.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.socket[0].bind((self.my_ip, self.port))
        self.socket[0].listen(10)

        while True:
            print("Waiting for senders on " + self.my_ip + ":" + str(self.port))
            connection, client = self.socket[0].accept()
            print("Receiving data from " + client[0] + ":" + str(client[1]))

            while True:
                data_raw = connection.recv(65565)
                if not data_raw:
                    print(client[0] + ":" + str(client[1]) + " Disconnected")
                    break

                data = data_raw.decode('utf-8')
                data = data.split(":")

                index = 1
                while index < len(data):

                    color = (int(data[index]), int(data[index+1]), int(data[index+2]))
                    if color != self.my_color:
                        if color not in self.queue_receiver:
                            self.queue_receiver[color] = []

                        if data[index+3] == "x":
                            self.queue_receiver[color].append("x")
                            self.queue_sender.append(":" + data[index] + ":" + data[index+1] + ":" + data[index+2] + ":x")
                            index = index + 4
                        else:
                            point = (int(data[index+3]), int(data[index+4]))
                            self.queue_receiver[color].append(point)
                            self.queue_sender.append(":" + data[index] + ":" + data[index+1] + ":" + data[index+2] + ":" + data[index+3] + ":" + data[index+4])
                            index = index + 5
                    else:
                        index = len(data)
