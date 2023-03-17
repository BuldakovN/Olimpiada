import pythonping

def ping(*args, **kwargs):
    kwargs['timeout'] = 1
    return pythonping.ping(*args, **kwargs)


