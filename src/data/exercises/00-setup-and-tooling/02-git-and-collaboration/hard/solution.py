def _walk(parents, starts):
    seen = set()
    stack = list(starts)
    while stack:
        c = stack.pop()
        if c in seen:
            continue
        seen.add(c)
        stack.extend(parents[c])
    return seen


def merge_base(parents, a, b):
    """Return the sorted list of best common ancestors of commits `a` and `b`."""
    for h in (a, b):
        if h not in parents:
            raise ValueError(f"unknown commit: {h!r}")
    common = _walk(parents, [a]) & _walk(parents, [b])
    # Everything strictly below some common ancestor is not a best one.
    below = _walk(parents, [p for c in common for p in parents[c]])
    return sorted(common - below)
