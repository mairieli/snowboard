import os
import locale
from dialog import Dialog

class Dialog_Connect:

    def __init__ (self, peer, created_board):
        self.peer = peer
        self.created_board = False

    def start(self):
        locale.setlocale(locale.LC_ALL, '')
        dialog = Dialog(dialog="dialog")
        dialog.set_background_title("Snowboard")

        code, server_ip = dialog.inputbox("Server IP:", width=0, height=0, title="Connect to Server", extra_label="Cool button")
        if code == dialog.OK:
            self.peer.server_ip = server_ip
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
                        self.created_board = self.peer.create_board(name)
                        if self.created_board == False:
                            os.system('clear')
                            print("Board " + name + " already exists")
                            exit()
                        else:
                            self.created_board = True
                else:
                    boards = self.peer.list_boards()
                    if boards[0] == "":
                        os.system('clear')
                        print("No boards on Server")
                        exit()
                    choices = []
                    for b in boards:
                        choices.append((b, ""))

                    code, board = dialog.menu("Choose a Board...", choices=choices)
                    if code == dialog.OK:
                        self.peer.connect(board)
                    else:
                        os.system('clear')
                        exit()
            else:
                os.system('clear')
                exit()
        else:
            os.system('clear')
            exit()
        os.system('clear')