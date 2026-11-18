import math
import random


def seeded_split(items, test_frac, seed):
    """Shuffle a copy of `items` with `seed`, then return (train, test)."""
    rng = random.Random(seed)
    shuffled = list(items)
    rng.shuffle(shuffled)
    n_test = math.ceil(len(shuffled) * test_frac)
    return shuffled[n_test:], shuffled[:n_test]
