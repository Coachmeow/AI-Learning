import math
import random


def seeded_split(items, test_frac, seed):
    shuffled = list(items)
    random.shuffle(shuffled)
    n_test = math.ceil(len(shuffled) * test_frac)
    return shuffled[n_test:], shuffled[:n_test]
