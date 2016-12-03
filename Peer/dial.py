import os
import locale
from dialog import Dialog

class Dialog_Connect:

    def __init__ (self, peer, created_board):
        self.peer = peer
        self.created_board = False
        self.dialog = Dialog(dialog="dialog")

    def exit_dialog(self):
        os.system('clear')
        exit()

    def boardname_dialog(self):
        code, name = self.dialog.inputbox("Board name:", width=0, height=0, title="Create a board", extra_label="Cool button")
        if code == self.dialog.OK:
            name = name.replace(" ", "")
            if name == "":
                os.system('clear')
                if self.dialog.yesno("Please, enter a valid name") == self.dialog.OK:
                    self.boardname_dialog()
                else:
                    self.exit_dialog()
            else:
                self.created_board = self.peer.create_board(name)
                if self.created_board == False:
                    os.system('clear')
                    if self.dialog.yesno("Board " + name + " already exists") == self.dialog.OK:
                        self.boardname_dialog()
                    else:
                        self.exit_dialog()
                else:
                    self.created_board = True
        else:
            self.options_board()

    def connect_dialog(self):
        boards = self.peer.list_boards()
        if boards[0] == "":
            os.system('clear')
            if self.dialog.yesno("No boards on Server") == self.dialog.OK:
                self.init_dialog()
        else:
            os.system('clear')
            choices = []
            for b in boards:
                choices.append((b, ""))

            code, board = self.dialog.menu("Choose a Board...", choices=choices)
            if code == self.dialog.OK:
                self.peer.connect(board)
            else:
                self.options_board()


    def options_board(self):
        code, tag = self.dialog.menu("You have two options:", choices=[("(1)", "Create a board"),("(2)", "Connect to board")])
        if code == self.dialog.OK:
            if tag == "(1)":
                self.boardname_dialog()
            else:
                self.connect_dialog()
        else:
            self.init_dialog()


    def init_dialog(self):
        code, server_ip = self.dialog.inputbox("Server IP:", width=0, height=0, title="Connect to Server", extra_label="Cool button")
        if code == self.dialog.OK:
            server_ip = server_ip.replace(" ", "")
            if server_ip == "":
                os.system('clear')
                self.init_dialog()
            else:
                self.peer.server_ip = server_ip
                self.options_board()
        else:
            self.exit_dialog()
        os.system('clear')


    def start(self):
        self.dialog.set_background_title("Snowboard")
        self.init_dialog()