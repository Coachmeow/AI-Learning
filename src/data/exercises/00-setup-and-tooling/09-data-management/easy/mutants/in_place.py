import math
import random


def seeded_split(items, test_frac, seed):
    random.Random(seed).shuffle(items)
    n_test = math.ceil(len(items) * test_frac)
    return items[n_test:], items[:n_test]
