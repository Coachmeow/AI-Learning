def _ancestors(parents, c, seen):
    if c in seen:
        return seen
    seen.add(c)
    for p in parents[c]:
        _ancestors(parents, p, seen)
    return seen


def merge_base(parents, a, b):
    if a not in parents or b not in parents:
        raise ValueError("unknown commit")
    common = _ancestors(parents, a, set()) & _ancestors(parents, b, set())
    below = set()
    for c in common:
        for p in parents[c]:
            _ancestors(parents, p, below)
    return sorted(common - below)
