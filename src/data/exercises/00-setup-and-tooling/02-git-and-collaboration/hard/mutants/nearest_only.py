from collections import deque


def merge_base(parents, a, b):
    if a not in parents or b not in parents:
        raise ValueError("unknown commit")
    from_a = set()
    q = deque([a])
    while q:
        c = q.popleft()
        if c not in from_a:
            from_a.add(c)
            q.extend(parents[c])
    q, seen = deque([b]), set()
    while q:
        c = q.popleft()
        if c in from_a:
            return [c]
        if c not in seen:
            seen.add(c)
            q.extend(parents[c])
    return []
