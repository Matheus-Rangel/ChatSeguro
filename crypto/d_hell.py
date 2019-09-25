import random

class Dhell():
    def __init__(self, prime=193, fi=5):
        self.prime = prime
        self.fi = fi
        r = random.Random()
        self.private_key = r.randrange(1, prime)
        self.public_key = int(self.fi ** self.private_key % self.prime)

    def generate_key(self, pair_key):
        return int(pair_key ** self.private_key % self.prime)
