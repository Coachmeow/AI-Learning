def _walk(parents, start):
    seen, stack = set(), [start]
    while stack:
        c = stack.pop()
        if c not in seen:
            seen.add(c)
            stack.extend(parents[c])
    return seen


def merge_base(parents, a, b):
    if a not in parents or b not in parents:
        raise ValueError("unknown commit")
    return sorted(_walk(parents, a) & _walk(parents, b))
