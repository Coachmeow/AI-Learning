import math
import random


def leak_free_split(texts, test_frac, seed):
    idx = list(range(len(texts)))
    random.Random(seed).shuffle(idx)
    chosen = set(idx[: math.ceil(len(texts) * test_frac)])
    return [t for i, t in enumerate(texts) if i not in chosen], [t for i, t in enumerate(texts) if i in chosen]
