import sys
import socket
import json
from enum import Enum
import curses
from .chat_net import ClientSocket, Status
def encrypt(msg, key):
    return msg

def handshake(sock, nick, chat_id, key):
    msg = {"nick": nick, "chat_id": chat_id, "key": key}
    status = sock.se

def start(server, port, chat_id, key):
    sock = ClientSocket()
    sock.connect(server, port)
    status = sock.handshake(chat_id, key)
    if status == Status.OK:
        print("AND THE GAME BEGINS")
        PRINT()
        pass
    elif status == Status.UNAUTHORIZED:
        print("YOU SHALL NOT PASS!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return
    elif status == Status.NOT_FOUND:
        print("YOU ARE LOST YOUR FOUL")
        return


if __name__ == "__main__":
    server = sys.argv[1]
    port = int(sys.argv[2])
    chat_id = sys.argv[3]
    key = sys.argv[4]
    curses.wrapper(start())