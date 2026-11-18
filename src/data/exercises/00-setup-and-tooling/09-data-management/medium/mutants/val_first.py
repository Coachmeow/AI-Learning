import hashlib


def hash_split(ids, val_frac=0.1, test_frac=0.1):
    v = round(val_frac * 100)
    t = round((test_frac + val_frac) * 100)
    out = {"train": [], "val": [], "test": []}
    for id_ in ids:
        bucket = int(hashlib.md5(id_.encode("utf-8")).hexdigest(), 16) % 100
        out["val" if bucket < v else "test" if bucket < t else "train"].append(id_)
    return out
