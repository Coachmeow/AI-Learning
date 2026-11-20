import math


def rope(vec, pos, base=10000.0):
    """Rotate each pair (vec[2j], vec[2j+1]) by pos * base ** (-2j / d)."""
    d = len(vec)
    if d == 0 or d % 2:
        raise ValueError("the vector length must be even and positive")
    out = []
    for j in range(d // 2):
        a = pos * base ** (-2 * j / d)
        x, y = vec[2 * j], vec[2 * j + 1]
        out.append(x * math.cos(a) - y * math.sin(a))
        out.append(x * math.sin(a) + y * math.cos(a))
    return out


def rope_score(q, k, m, n, base=10000.0):
    """Dot product of rope(q, m, base) and rope(k, n, base)."""
    return sum(a * b for a, b in zip(rope(q, m, base), rope(k, m, base)))
