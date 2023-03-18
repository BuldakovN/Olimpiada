import socket
from socket import AF_INET, SOCK_STREAM

class Socket(socket.socket):
    """
    Класс-адаптер сокета
    """
    def __init__(self):
        super().__init__(AF_INET, SOCK_STREAM)
        self.settimeout(1)

    @staticmethod
    def gethostbyname_ex(*args, **kwargs):
        """
        gethostbyname_ex получение информации о хосте по имени
        """
        return socket.gethostbyname_ex(*args, **kwargs)
