import random
import endpoint

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

if __name__ == '__main__':
    endpoints = endpoint.get_endpoints()

    lb = RandomLoadBalancer(endpoints)
    endpoint = lb.balance_load()
