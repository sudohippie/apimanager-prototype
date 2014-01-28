import random
import endpoint
import hashlib

class RandomLoadBalancer:
    endpoints = []

    def __init__(self, endpoints=[]):
        self.endpoints = endpoints

    def balance_load(self):
        # preconditions
        if self.endpoints is None or len(self.endpoints) == 0:
            return None

        # generate random number
        max_range = len(self.endpoints) * 100
        rand = random.uniform(0, max_range)
        endpoint = self.endpoints[int(rand / 100)]

        print self.__class__.__name__ + ': ' + endpoint.to_string()

        # return appropriate end point
        return endpoint

class WeightedRandomLoadBalancer:
    weighted_endpoints = {}
    range = 0

    def __init__(self, weighted_endpoints={}):
        self.weighted_endpoints = weighted_endpoints
        self.recalculate_range()

    def add_endpoint(self, endpoint, weight):
        self.weighted_endpoints[endpoint] = weight
        self.recalculate_range()

    def recalculate_range(self):
        # sum all weights
        max = 0
        for weight in self.weighted_endpoints.values():
            max += int(weight)
        self.range = max

    def balance_load(self):
        # preconditions
        if self.weighted_endpoints is None:
            return None

        # generate random number
        rand = int(random.uniform(0, self.range*100))

        # identify the assignable host, check cumulative sum
        cum_total = 0
        keys = self.weighted_endpoints.keys()
        endpoint = None
        for key in keys:
            cum_total += int(self.weighted_endpoints[key])
            if rand < cum_total*100:
                endpoint = key
                break

        print self.__class__.__name__ + ': ' + endpoint.to_string()

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

        # random load balancer
        #lb = RandomLoadBalancer(endpoints)
        #endpoint = lb.balance_load()

        # weighter random load banlancer
        lb = WeightedRandomLoadBalancer()
        for index in range(0, len(endpoints)):
            lb.add_endpoint(endpoints[index], index + 10)
        endpoint = lb.balance_load()

        # consistent hash load balancer
        #lb = ConsistentHashLoadBalancer(endpoints)
        #endpoint = lb.balance_load('/da')

        print endpoint.to_string()

