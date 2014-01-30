import random
import endpoint
import hashlib
import re

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

class HashLoadBalancer:
    endpoints = []

    def __init__(self, endpoints=[]):
        self.endpoints = endpoints

    def hash(self, str):
        hash_value = hashlib.md5(str)
        return long(hash_value.hexdigest()[0:16], base=16)

    def balance_load(self, str):
        # precondition
        if self.endpoints is None or not self.endpoints or str is None:
            return None

        # calculate hash
        input_hash = self.hash(str)

        # determine endpoint
        endpoint = self.endpoints[input_hash % len(endpoints)]

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
        # taking on first 16 hex, to make hash sensitive
        return long(hash_value.hexdigest()[0:16], base=16)

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

class RoundRobinLoadBalancer:
    endpoints = []
    last_index = -1

    def __init__(self, endpoints=[]):
        self.endpoints = endpoints

    def balance_load(self):
        # preconditions
        if self.endpoints is None or not self.endpoints:
            return None

        # calculate index and return endpoint
        index = (self.last_index + 1) % len(self.endpoints)
        endpoint = self.endpoints[index]
        self.last_index = index

        print self.__class__.__name__ + ': ' + endpoint.to_string()

        return endpoint

class PatternMatchLoadBalancer:
    endpoints = {}

    def __init__(self, endpoints={}):
        self.endpoints = endpoints

    def add_pattern(self, pattern, endpoint):
        # preconditions
        if pattern is None or endpoint is None:
            return

        # compile pattern
        self.endpoints[re.compile(pattern)] = endpoint

    def balance_load(self, str):
        # preconditions
        if str is None:
            return None

        # match string to pattern
        patterns = self.endpoints.keys()
        for pattern in patterns:
            match = pattern.match(str)
            # if found, return host
            if match is not None:
                endpoint = self.endpoints[pattern]
                print self.__class__.__name__ + ': ' + endpoint.to_string()
                return endpoint

        return None

class DynamicLoadBalancer:
    endpoints = []
    threshold = 50

    def __init__(self, endpoints=[], threshold=50):
        self.endpoints = endpoints
        self.threshold = threshold

    def balance_load(self):
        # preconditions
        if self.endpoints is None or len(self.endpoints) == 0:
            return None

        min_load = 100
        min_load_ep = None
        # find endpoint with least load
        for ep in self.endpoints:
            load = ep.get_load()
            if load < min_load:
                min_load = load
                min_load_ep = ep

        # if endpoint is with in thresh hold, return
        if min_load <= self.threshold:
            print self.__class__.__name__ + ': ' + min_load_ep.to_string() + ': Load=' + str(min_load)
            return min_load_ep

        return None

if __name__ == '__main__':
        endpoints = endpoint.get_endpoints()

        # random load balancer
        #lb = RandomLoadBalancer(endpoints)
        #endpoint = lb.balance_load()

        # weighter random load banlancer
        #lb = WeightedRandomLoadBalancer()
        #for index in range(0, len(endpoints)):
        #    lb.add_endpoint(endpoints[index], index + 10)
        #endpoint = lb.balance_load()

        # consistent hash load balancer
        #lb = ConsistentHashLoadBalancer(endpoints)
        #endpoint = lb.balance_load('/sdfa/23')

        # round robin load balancer
        #lb = RoundRobinLoadBalancer(endpoints)
        #endpoint = lb.balance_load()

        # consistent hash load balancer
        #lb = HashLoadBalancer(endpoints)
        #endpoint = lb.balance_load('/sdfa')

        # pattern match load balancer
        #lb = PatternMatchLoadBalancer()
        #lb.add_pattern(r'([/a-zA-Z0-9]+)?/[0-9]+[^a-zA-Z]+', endpoints[0])
        #lb.add_pattern(r'([/a-zA-Z0-9]+)?/[a-z]+[^A-Z0-9]+', endpoints[1])
        #lb.add_pattern(r'([/a-zA-Z0-9]+)?/[A-Z]+[^0-9a-z]+', endpoints[2])
        #endpoint = lb.balance_load('/abdf')

        # dynamic load balancer
        lb = DynamicLoadBalancer(endpoints, 70)
        endpoint = lb.balance_load()

        if endpoint is None:
            print None


