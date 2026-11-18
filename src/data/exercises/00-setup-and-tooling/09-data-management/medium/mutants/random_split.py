import random


def hash_split(ids, val_frac=0.1, test_frac=0.1):
    rng = random.Random(len(ids))
    out = {"train": [], "val": [], "test": []}
    for id_ in ids:
        r = rng.random()
        out["test" if r < test_frac else "val" if r < test_frac + val_frac else "train"].append(id_)
    return out
