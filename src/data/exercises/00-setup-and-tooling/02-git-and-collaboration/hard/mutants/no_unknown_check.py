def _walk(parents, starts):
    seen, stack = set(), list(starts)
    while stack:
        c = stack.pop()
        if c not in seen:
            seen.add(c)
            stack.extend(parents.get(c, []))
    return seen


def merge_base(parents, a, b):
    common = _walk(parents, [a]) & _walk(parents, [b])
    below = _walk(parents, [p for c in common for p in parents.get(c, [])])
    return sorted(common - below)
