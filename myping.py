import pythonping

def ping(*args, **kwargs):
    kwargs['timeout'] = 5
    return pythonping.ping(*args, **kwargs)


