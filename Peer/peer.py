import os
import socket
import locale
from sender import Sender
from dialog import Dialog
from listener import Listener
from whiteboard import Whiteboard
from listenerudp import Listener_UDP

class Peer:

    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host_ip = "192.168.1.109"
        self.host_port = 6000
        self.current_board = ""
        self.ips = []
        self.queue_receiver = {}
        self.queue_sender = []
        self.my_color = (255, 0, 255)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        self.my_ip = s.getsockname()[0]

    def list_boards(self):
        self.socket.sendto("list all".encode('utf-8'), (self.host_ip, self.host_port))
        msg, server = self.socket.recvfrom(65565)
        return msg.decode('utf-8').split(":")

    def create_board(self, board_name):
        message = "create " + board_name
        self.socket.sendto(message.encode('utf-8'), (self.host_ip, self.host_port))

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
        self.socket.sendto(message.encode('utf-8'), (self.host_ip, self.host_port))

    def connect(self, board_name):
        message = "connect " + board_name
        self.current_board = board_name
        self.socket.sendto(message.encode('utf-8'), (self.host_ip, self.host_port))

        response, server = self.socket.recvfrom(65565)
        ips = response.decode('utf-8').split(":")
        for ip in ips:
            if ip != self.my_ip:
                self.ips.append(ip)
        self.ips.append(self.my_ip)

if __name__ == '__main__':
    print("Starting Peer...")
    peer = Peer()

    locale.setlocale(locale.LC_ALL, '')
    dialog = Dialog(dialog="dialog")
    dialog.set_background_title("Snowboard")

    created = False

    code, tag = dialog.menu("You have two options:", choices=[("(1)", "Create a board"),("(2)", "Connect to board")])
    if code == dialog.OK:
        if tag == "(1)":
            code, name = dialog.inputbox("Board name:", width=0, height=0, title="Create a board", extra_label="Cool button")
            name = name.replace(" ", "")
            if name == "":
                os.system('clear')
                print("Please, enter a valid name")
                exit()
            else:
                created = peer.create_board(name)
                if created == False:
                    os.system('clear')
                    print("Board " + name + " already exists")
                    exit()
                else:
                    created = True
        else:
            boards = peer.list_boards()
            choices = []
            for b in boards:
                choices.append((b, ""))

            code, board = dialog.menu("Choose a Board...", choices=choices)
            if code == dialog.OK:
                peer.connect(board)
    else:
        os.system('clear')
        exit()

    os.system('clear')
    print("Connected to Board: " + peer.current_board)

    print("Starting Listener...")
    listener = Listener(peer.my_color, peer.queue_receiver, peer.queue_sender, peer.ips, peer.my_ip)
    listener.start()

    if not created:
        last_ip = peer.ips[len(peer.ips) - 2]
        msg = "connect " + peer.my_ip
        peer.socket.sendto(msg.encode('utf-8'), (last_ip, 5002))
        print("Sending connect to " + last_ip + ":5002")

    print("Starting Whiteboard...")
    w = Whiteboard(peer.my_color, peer.queue_receiver, peer.queue_sender)
    w.start()

    print("Starting Listener UDP...")
    listenerudp = Listener_UDP(peer.ips, peer.my_ip)
    listenerudp.start()

    print("Starting Sender...")
    sender = Sender(peer.queue_sender, peer.ips, peer.my_ip)
    sender.start()