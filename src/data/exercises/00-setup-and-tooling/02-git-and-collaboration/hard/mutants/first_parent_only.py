def _walk(parents, starts):
    seen, stack = set(), list(starts)
    while stack:
        c = stack.pop()
        if c not in seen:
            seen.add(c)
            stack.extend(parents[c][:1])
    return seen


def merge_base(parents, a, b):
    if a not in parents or b not in parents:
        raise ValueError("unknown commit")
    common = _walk(parents, [a]) & _walk(parents, [b])
    below = _walk(parents, [p for c in common for p in parents[c][:1]])
    return sorted(common - below)
