import pythonping


class Ping:
    """
     Класс-адаптер для пингования
    """
    @staticmethod
    def ping(*args, **kwargs):
        kwargs['timeout'] = 1
        return pythonping.ping(*args, **kwargs)


