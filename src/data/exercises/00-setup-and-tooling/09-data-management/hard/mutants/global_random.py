import math
import random
import string

_STRIP = str.maketrans("", "", string.punctuation)


def leak_free_split(texts, test_frac, seed):
    groups = {}
    for i, t in enumerate(texts):
        groups.setdefault(" ".join(t.lower().translate(_STRIP).split()), []).append(i)
    order = list(groups.values())
    random.shuffle(order)
    target = math.ceil(len(texts) * test_frac)
    chosen = set()
    for g in order:
        if len(chosen) >= target:
            break
        chosen.update(g)
    return [t for i, t in enumerate(texts) if i not in chosen], [t for i, t in enumerate(texts) if i in chosen]
