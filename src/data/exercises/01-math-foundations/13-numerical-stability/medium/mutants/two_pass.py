def welford(xs):
    """(mean, population variance) of xs in one pass with Welford's algorithm."""
    if len(xs) == 0:
        raise ValueError("welford() needs at least one value")
    mean = sum(xs) / len(xs)
    return mean, sum((x - mean) ** 2 for x in xs) / len(xs)
