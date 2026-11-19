def welford(xs):
    """(mean, population variance) of xs in one pass with Welford's algorithm."""
    n, mean, m2 = 0, 0.0, 0.0
    for x in xs:
        n += 1
        delta = x - mean
        mean += delta / n
        m2 += delta * (x - mean)
    if n == 0:
        raise ValueError("welford() needs at least one value")
    return mean, m2 / n
