def hash_split(ids, val_frac=0.1, test_frac=0.1):
    t = round(test_frac * 100)
    v = round((test_frac + val_frac) * 100)
    out = {"train": [], "val": [], "test": []}
    for id_ in ids:
        bucket = hash(id_) % 100
        out["test" if bucket < t else "val" if bucket < v else "train"].append(id_)
    return out
