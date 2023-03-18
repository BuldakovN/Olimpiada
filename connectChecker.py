import re
from mysocket import Socket
from myping import Ping
from datetime import datetime


class ConnectChecker:
    """
     Класс соединения. Хранит адрес и порты, осуществляет проверку соединения по адресу и портам
    """
    def __init__(self, hostname, ports):
        self.hostname, self.ip_list = self.__addressParser(hostname)
        self.ports = self.__portsParser(ports)

    def __addressParser(self, hostname):
        """
        Обработка адресов
        """
        
        # является ли hostname ip-адресом
        is_ip = (
            re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", hostname)
            is not None
        )
        if is_ip:
            
            # если ip-адрес
            ip_list = [hostname]
            hostname = "????????"
        else:
            
            # получаем все ip-адреса по данному имени
            try:
                ip_list = Socket.gethostbyname_ex(hostname)[2]
            except:
                raise "Данное доменное имя не найдено или нет соединения с интернетом"
        return hostname, ip_list

    def __portsParser(self, ports):
        """
        Обработка портов
        """
        ports = ports.split(",")
        new_ports = []
        for port in ports:
            try:
                
                # будем брать только те порты, которые представлены целым числом
                new_ports.append(int(port))
            except:
                pass
        return new_ports

    def __pingSite(self):
        """
        __pingSite _summary_

        Yields:
            str: строка с информацией о результате проверки очередного адреса
        """
        print(
            "|{:^19}|{:^20}|{:^15}|{:^7}|{:^7}".format(
                "Время", "Имя хоста", "IP-адрес", "Статус", 'Пинг'
            )
        )
        for ip in self.ip_list:
            ping_result = Ping.ping(ip, count=3)
            line: str = "|{:^19}|{:^20}|{:^15}|{:^7}|{:^7}"
            line: str = line.format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.hostname,
                ip,
                "OK" if ping_result.success(2) else "FALSE",
                str(ping_result.rtt_avg_ms) + ' ms'
            )
            yield line

    def __portIsOpen(self, ip: str, port: int):
        """
        __portIsOpen проверка открытости порта

        Args:
            ip (str): ip адрес
            port (int): порт

        Returns:
            bool: результат (True или False)
        """
        sock = Socket()
        result: bool = sock.connect_ex((ip, port)) == 0
        sock.close()
        return result

    def __checkPorts(self):
        """
        __checkPorts провека открытости портов для данного хоста

        Yields:
            str: строка с информацией о результате проверки очередного адреса
        """
        print(
            "|{:^20}|{:^20}|{:^15}|{:^5}|{:^10}|{:^10}".format(
                "Время", "Имя хоста", "IP-адрес", "Порт", "Открытость", "Пинг"
            )
        )
        for ip in self.ip_list:
            for port in self.ports:
                isOpen = self.__portIsOpen(ip, port)
                line = "|{:^20}|{:^20}|{:^15}|{:^5}|{:^10}|{:^10}"
                ping_result = Ping.ping(ip, count=2).rtt_avg_ms
                line: str = line.format(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.hostname,
                    ip,
                    port,
                    "Открыт" if isOpen else "Закрыт",
                    str(ping_result) + ' ms' if isOpen else "---" 
                )
                yield line

    def checkConnection(self):
        """
        checkConnection запуск проверки соединения для данного хоста

        Returns:
            _type_: _description_
        """
        if self.hostname is None and self.ip_list is None:
            return ""
        
        # если порты не указаны, то просто пингуем
        if len(self.ports) == 0:
            return self.__pingSite()
        
        # если указаны, то проверяем все порты для каждого ip-адреса
        return self.__checkPorts()

    def __repr__(self):
        """
        __repr__ краткая информация об экземляре класса

        Returns:
            str: выводимая информация
        """
        result: str = "Имя хоста: " + self.hostname
        result += ", IP-адреса: " + str(self.ip_list)
        result += ", порты: " + str(self.ports)
        return result
