import random
from math import pow
class Dhell():
    def __init__(self, prime = 193, fi = 5):
        self.prime = prime
        self.fi = 5
        r = random.Random()
        self.private_key = r.randrange(1, prime)
        self.public_key = (self.fi * self.private_key) % self.prime
    def generate_key(self, pair_key):
        return pow(pair_key, self.private_key) % self.prime