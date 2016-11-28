from threading import Thread
import socket

class Listener(Thread):
    def __init__ (self, my_color, queue_receiver, queue_sender, ips):
        Thread.__init__(self)
        self.host = ''
        self.port =  5001
        self.queue_receiver = queue_receiver
        self.queue_sender = queue_sender
        self.my_color = my_color
        self.ips = ips

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(10)

        last_ip = self.ips[len(self.ips) - 1]
        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_udp.sendto("connect".encode('utf-8'), (last_ip, 5002))

        while True:
            print("Waiting for senders on " + socket.gethostbyname(socket.gethostname()) + ":" + str(self.port))
            connection, client = s.accept()
            print("Receiving data from " + client[0] + ":" + str(client[1]))
            while True:
                data_raw = connection.recv(65565)
                if not data_raw:
                    print(client[0] + ":" + str(client[1]) + " Disconnected")
                    break

                data = data_raw.decode('utf-8')
                print("Received '" + data + "'")
                data = data.split(":")

                index = 1
                while 1 < len(data)
                color = (int(data[index]), int(data[index+1]), int(data[index+2]))

                if color != self.my_color:
                    if color not in self.queue_receiver:
                        self.queue_receiver[color] = []

                    self.queue_sender.append(data_raw)
                    if data[index+3] == "x":
                        self.queue_receiver[color].append("x")
                        index = index + 4
                    else:
                        point = (int(data[index+3]), int(data[index+4]))
                        self.queue_receiver[color].append(point)
                        index = index + 5