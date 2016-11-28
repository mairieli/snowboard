from threading import Thread
import socket

class Listener(Thread):
    def __init__ (self, my_color, queue_receiver, queue_sender):
        Thread.__init__(self)
        self.host = ''
        self.port =  5001
        self.queue_receiver = queue_receiver
        self.queue_sender = queue_sender
        self.my_color = my_color

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(10)
        while True:
            connection, client = s.accept()
            while True:
                data = connection.recv(65565)
                if not data:
                    break

                data = data.decode('utf-8')
                self.queue_sender.append(data)
                data = data.split(":")
                color = (data[0], data[1], data[2])

                if color != my_color:
                    if data[3] == "x":
                        self.queue_receiver[color].append("x")
                    else:
                        point = (data[3], data[4])
                        if color in self.queue_receiver
                            self.queue_receiver[color].append(point)
                        else:
                            self.queue_receiver[color] = []
                            self.queue_receiver[color].append(point)