import random

class SimpleEndpoint:
    host = ''
    port = 0
    scheme = 'http'

    def __init__(self, host, port, scheme='http'):
        self.host = host
        self.port = port
        self.scheme = scheme

    def to_string(self):
        return 'host=' + self.host + ', port=' + str(self.port) + ', scheme=' + self.scheme

    def get_load(self):
        # get hour of time
        hour = int(random.uniform(0, 24))
        # if its during the day, the load is higher
        if hour >= 7 <= 20:
            return int(random.uniform(75, 101))
        else:
            return int(random.uniform(0, 90))

def get_single_endpoint():
    host = SimpleEndpoint('localhost', 8084)
    return host

def get_endpoints():
    #host = SimpleEndpoint('localhost', 8084)
    host0 = SimpleEndpoint('localhost-0', 8084)
    host1 = SimpleEndpoint('localhost-1', 8084)
    host2 = SimpleEndpoint('localhost-2', 8084)
    host3 = SimpleEndpoint('localhost-3', 8084)
    host4 = SimpleEndpoint('localhost-4', 8084)
    host5 = SimpleEndpoint('localhost-5', 8084)

    host_list = [host0, host1, host2, host3, host4, host5]

    return host_list
