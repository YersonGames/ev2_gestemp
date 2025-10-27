import base64

def encriptar(data):
    d = base64.b64encode(data.encode()).decode()
    return d

def desencriptar(data):
    d = base64.b64decode(data.encode()).decode()
    return d