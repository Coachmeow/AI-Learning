def welford(xs):
    """(mean, population variance) of xs in one pass with Welford's algorithm."""
    n, s, s2 = 0, 0.0, 0.0
    for x in xs:
        n += 1
        s += x
        s2 += x * x
    if n == 0:
        raise ValueError("welford() needs at least one value")
    mean = s / n
    return mean, s2 / n - mean * mean
