from threading import Thread
import socket

class Worker(Thread):
    def __init__ (self, msg, client, table):
        Thread.__init__(self)
        self.table = table
        self.msg = msg.decode('utf-8')
        self.client_ip = client[0]
        self.client_port = client[1]
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        print("Message from " + self.client_ip + ":" + str(self.client_port) + " => " + self.msg)

        name_board = self.msg.split(" ")[1]
        if self.msg.startswith("create"):
            if name_board in self.table:
                print("\tBoard " + name_board + " already exists")
                self.s.sendto("board exists".encode('utf-8'), (self.client_ip, self.client_port))

            else:
                print("\tCreated Board: " + name_board)
                self.table[name_board] = []
                print("\tAdded " + self.client_ip + " to " + name_board)
                self.table[name_board].append(self.client_ip)
                self.s.sendto("created".encode('utf-8'), (self.client_ip, self.client_port))

        elif self.msg.startswith("list all"):
            response = ""
            for board in self.table.keys():
                if response == "":
                    response = board
                else:
                    response = response + ":" + board
            print("\tSend '" + response + "' to " + self.client_ip)
            self.s.sendto(response.encode('utf-8'), (self.client_ip, self.client_port))

        elif self.msg.startswith("connect"):
            response = ""
            for ip in self.table[name_board]:
                if response == "":
                    response = ip
                else:
                    response = response + ":" + ip
            print("\tSend '" + response + "' to " + self.client_ip)
            self.s.sendto(response.encode('utf-8'), (self.client_ip, self.client_port))
            print("\tAdded " + self.client_ip + " to " + name_board)
            self.table[name_board].append(self.client_ip)

        elif self.msg.startswith("disconnect"):
            print("\tRemoved " + self.client_ip + " to " + name_board)
            self.table[name_board].remove(self.client_ip)
            if len(self.table[name_board]) == 0:
                print("\tDeleted Board: " + name_board + ", because is empty")
                self.table.pop(name_board)

        print()