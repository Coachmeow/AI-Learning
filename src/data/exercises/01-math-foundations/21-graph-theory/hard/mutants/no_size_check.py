import math


def fiedler_split(n, edges):
    """Return (labels, fiedler_value) from power iteration on c*I - L."""
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    if len(seen) != n:
        raise ValueError("the graph is not connected")

    def lap(x):
        return [len(adj[i]) * x[i] - sum(x[j] for j in adj[i]) for i in range(n)]

    c = 2 * max(len(a) for a in adj) + 1
    v = [math.sin(i + 1) for i in range(n)]
    for _ in range(20000):
        Lv = lap(v)
        w = [c * v[i] - Lv[i] for i in range(n)]
        mean = sum(w) / n
        w = [x - mean for x in w]
        norm = math.sqrt(sum(x * x for x in w))
        w = [x / norm for x in w]
        done = math.sqrt(sum((a - b) ** 2 for a, b in zip(w, v))) < 1e-12
        v = w
        if done:
            break
    Lv = lap(v)
    value = sum(a * b for a, b in zip(v, Lv)) / sum(a * a for a in v)
    labels = [0 if (x > 0) == (v[0] > 0) else 1 for x in v]
    return labels, value
