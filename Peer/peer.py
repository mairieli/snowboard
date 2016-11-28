import socket
from listener import Listener
from listenerudp import Listener_UDP
from sender import Sender
from whiteboard import Whiteboard

class Peer:

    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 5000))
        self.host_ip = "192.168.1.109"
        self.host_port = 5000
        self.current_board = ""
        self.ips = []
        self.queue_receiver = {}
        self.queue_sender = []
        self.my_color = (0, 0, 0)

    def list_boards(self):
        self.socket.sendto("list all".encode('utf-8'), (self.host_ip, self.host_port))
        msg, server = self.socket.recvfrom(65565)
        return msg.decode('utf-8').split(":")

    def create_board(self, board_name):
        message = "create " + board_name
        self.socket.sendto(message.encode('utf-8'), (self.host_ip, self.host_port))

        response, server = self.socket.recvfrom(65565)
        response = response.decode('utf-8')
        if response.decode('utf-8') == "created":
            self.current_board = board_name

    def disconnect(self):
        message = "disconnect " + self.current_board
        self.socket.sendto(message.encode('utf-8'), (self.host_ip, self.host_port))

    def connect(self, board_name):
        message = "connect " + board_name
        self.socket.sendto(message.encode('utf-8'), (self.host_ip, self.host_port))

        response, server = self.socket.recvfrom(65565)
        ips = response.decode('utf-8').split(":")
        for ip in ips:
            self.ips.append(ip)
        return self.ips

if __name__ == '__main__':
    print("Starting Peer...")

    peer = Peer()
    listener = Listener(peer.my_color, peer.queue_receiver, peer.queue_sender)
    listener.start()

    listenerudp = Listener_UDP(peer.ips)
    listenerudp.start()

    sender = Sender(peer.queue_sender, peer.ips)
    sender.start()

    w = Whiteboard(peer.my_color, peer.queue_receiver, peer.queue_sender)