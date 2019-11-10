class Randomness:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = int((self.seed * 1664525 + 1013904223) % 4294967296)
        # print(str(self.seed) + " -> ", end='')
        return self.seed

    def next_random_number(self, min_val, max_val):
        if min_val >= max_val:
            return min_val
        result = min_val + int(self.next() % (1 + max_val - min_val))
        return result
