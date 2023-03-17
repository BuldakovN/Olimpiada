import socket
from socket import AF_INET, SOCK_STREAM

class Socket(socket.socket):
    def __init__(self):
        super().__init__(AF_INET, SOCK_STREAM)
        self.settimeout(1)


def gethostbyname_ex(*args, **kwargs):
    return socket.gethostbyname_ex(*args, **kwargs)
