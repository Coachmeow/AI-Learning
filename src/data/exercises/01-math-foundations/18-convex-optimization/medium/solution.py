def closest_point(c, a, b):
    """Minimize ||x - c||^2 subject to a . x = b.

    Return (x, lam), where lam is the multiplier in
    L = ||x - c||^2 + lam * (a . x - b).
    """
    aa = sum(ai * ai for ai in a)
    if aa == 0:
        raise ValueError("a must not be the zero vector")
    ac = sum(ai * ci for ai, ci in zip(a, c))
    lam = 2 * (ac - b) / aa
    x = [ci - lam / 2 * ai for ci, ai in zip(c, a)]
    return x, lam
