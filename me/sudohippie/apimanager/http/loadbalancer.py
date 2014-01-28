import random
import endpoint
import hashlib

class RandomLoadBalancer:
    endpoints = []

    def __init__(self, endpoints):
        self.endpoints = endpoints

    def balance_load(self):
        # preconditions
        if self.endpoints is None or len(self.endpoints) == 0:
            return None

        # generate random number
        max_range = len(self.endpoints) * 100 - 1
        rand = random.uniform(0, max_range)
        endpoint = self.endpoints[int(rand % len(self.endpoints))]

        print self.__class__.__name__ + ': ' + endpoint.to_string()

        # return appropriate end point
        return endpoint

class ConsistentHashLoadBalancer:
    endpoints = []
    hashes = {}

    def __init__(self, endpoints):
        self.endpoints = endpoints

        # calculate hashes
        if self.endpoints is not None:
            for endpoint in endpoints:
                hash_key = self.hash(endpoint.host + ':' + str(endpoint.port))
                self.hashes[hash_key] = endpoint

    def hash(self, str):
        hash_value = hashlib.md5(str)
        return long(hash_value.hexdigest(), base=16)

    def balance_load(self, str):
        # preconditions
        if self.hashes is None or len(self.hashes) == 0 or str is None:
            return None

        # generate hash for input
        input_hash = self.hash(str)

        # compare input vs hash ring
        sorted_keys = self.hashes.keys()
        sorted_keys.sort()

        for index in range(0, len(sorted_keys)):
            hash_key = sorted_keys[index]
            if long(input_hash) < long(hash_key):
                break

        # edge case, when input is smaller than all keys in ring
        if index - 1 < 0:
            index = len(self.hashes)

        endpoint = self.hashes[sorted_keys[index - 1]]

        print self.__class__.__name__ + ': ' + endpoint.to_string()

        # return value
        return endpoint

if __name__ == '__main__':
        endpoints = endpoint.get_endpoints()

        #lb = RandomLoadBalancer(endpoints)
        #endpoint = lb.balance_load()

        lb = ConsistentHashLoadBalancer(endpoints)
        endpoint = lb.balance_load('/da')

        print endpoint.to_string()

