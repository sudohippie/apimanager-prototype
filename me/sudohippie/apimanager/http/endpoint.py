class Host:
    host = ''
    port = 0
    scheme = 'http'

    def __init__(self, host, port, scheme='http'):
        self.host = host
        self.port = port
        self.scheme = scheme

    def to_string(self):
        return 'host=' + self.host + ', port=' + str(self.port) + ', scheme=' + self.scheme



def get_single_endpoint():
    host = Host('localhost', 8084)
    return host

def get_endpoints():
    host = Host('localhost', 8084)
    host0 = Host('localhost0', 8084)
    host1 = Host('localhost1', 8084)
    host2 = Host('localhost2', 8084)
    host3 = Host('localhost3', 8084)
    host4 = Host('localhost4', 8084)
    host5 = Host('localhost5', 8084)

    host_list = [host, host0, host1, host2, host3, host4, host5]

    return host_list
