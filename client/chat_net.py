from enum import Enum
import socket

class Status(Enum):
    OK = 200
    UNAUTHORIZED = 401
    NOT_FOUND = 404

class ClientSocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        totalsent = 0
        sent = self.sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        return self.myreceive()
    def receive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

def connect(server, port, chat_id, key):
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((server, port))
    s.sen
    return socket