import sys
import time
import socket
from sender import Sender
from dial import Dialog_Connect
from random import randint
from listener import Listener
from whiteboard import Whiteboard
from listenerudp import Listener_UDP

class Peer:

    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_ip = ""
        self.host_port = 6000
        self.current_board = ""
        self.ips = []
        self.queue_receiver = {}
        self.queue_sender = []
        self.my_color = (randint(0,254), randint(0,254), randint(0,254))

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 53))
            self.my_ip = s.getsockname()[0]
        except Exception as e:
            print("MY IP: ", end="")
            self.my_ip = input()
        s.close()

    def list_boards(self):
        self.socket.sendto("list all".encode('utf-8'), (self.server_ip, self.host_port))
        msg, server = self.socket.recvfrom(65565)
        return msg.decode('utf-8').split(":")

    def create_board(self, board_name):
        message = "create " + board_name
        self.socket.sendto(message.encode('utf-8'), (self.server_ip, self.host_port))

        response, server = self.socket.recvfrom(65565)
        response = response.decode('utf-8')
        if response == "created":
            self.current_board = board_name
            self.ips.append(self.my_ip)
            return True
        else:
            return False

    def disconnect(self):
        message = "disconnect " + self.current_board
        self.socket.sendto(message.encode('utf-8'), (self.server_ip, self.host_port))

    def connect(self, board_name):
        message = "connect " + board_name
        self.current_board = board_name
        self.socket.sendto(message.encode('utf-8'), (self.server_ip, self.host_port))

        response, server = self.socket.recvfrom(65565)
        ips = response.decode('utf-8').split(":")
        for ip in ips:
            if ip != self.my_ip:
                self.ips.append(ip)
        self.ips.append(self.my_ip)

if __name__ == '__main__':
    peer = Peer()

    created_board = False
    Dialog_Connect(peer, created_board).start()
    print("CONNECTED TO BOARD: " + peer.current_board)

    socket_listener = [True]
    listener = Listener(peer.my_color, peer.queue_receiver, peer.queue_sender, peer.ips, peer.my_ip, socket_listener)
    listener.start()

    time.sleep(1)

    if not created_board:
        last_ip = peer.ips[len(peer.ips) - 2]
        first_ip = peer.ips[0]
        msg = "connect " + peer.my_ip
        peer.socket.sendto(msg.encode('utf-8'), (last_ip, 5002))
        peer.socket.sendto(msg.encode('utf-8'), (first_ip, 5002))
        print("\tSending connect to " + last_ip + ":5002")
        print("\tSending connect to " + first_ip + ":5002")

    close = []
    close.append(False)
    whiteboard = Whiteboard(peer.my_color, peer.queue_receiver, peer.queue_sender, close)
    whiteboard.start()

    socket_listenerudp = [True]
    listenerudp = Listener_UDP(peer.ips, peer.my_ip, socket_listenerudp)
    listenerudp.start()

    socket_sender = [True]
    sender = Sender(peer.queue_sender, peer.ips, peer.my_ip, peer.current_board, peer.server_ip, socket_sender)
    sender.start()

    while True:
        if close[0] == True:
            peer.disconnect()
            print("---Disconnect to Server")
            if peer.socket != None:
                peer.socket.close()
            if socket_sender[0] != True:
                socket_sender[0].close()
                print("---Stop send")
            if socket_listener[0] != True:
                socket_listener[0].close()
                print("---Stop Listener")
            if socket_listenerudp[0] != True:
                socket_listenerudp[0].close()
                print("---Stop Listener UDP")
            sys.exit()