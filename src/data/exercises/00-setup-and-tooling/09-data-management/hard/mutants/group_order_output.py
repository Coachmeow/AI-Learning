import math
import random
import string

_STRIP = str.maketrans("", "", string.punctuation)


def leak_free_split(texts, test_frac, seed):
    groups = {}
    for i, t in enumerate(texts):
        groups.setdefault(" ".join(t.lower().translate(_STRIP).split()), []).append(i)
    order = list(groups.values())
    random.Random(seed).shuffle(order)
    target = math.ceil(len(texts) * test_frac)
    test, train = [], []
    for g in order:
        (test if len(test) < target else train).extend(texts[i] for i in g)
    return train, test
