import math
import random
import string

_STRIP = str.maketrans("", "", string.punctuation)


def _normalise(text):
    return " ".join(text.lower().translate(_STRIP).split())


def leak_free_split(texts, test_frac, seed):
    """(train, test) where duplicate texts (after normalising) always land in the same split."""
    groups = {}
    for i, t in enumerate(texts):
        groups.setdefault(_normalise(t), []).append(i)
    order = list(groups.values())
    random.Random(seed).shuffle(order)
    target = math.ceil(len(texts) * test_frac)
    chosen = set()
    for group in order:
        if len(chosen) >= target:
            break
        chosen.update(group)
    train = [t for i, t in enumerate(texts) if i not in chosen]
    test = [t for i, t in enumerate(texts) if i in chosen]
    return train, test
