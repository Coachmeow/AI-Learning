def closest_point(c, a, b):
    """Minimize ||x - c||^2 subject to a . x = b.

    Return (x, lam), where lam is the multiplier in
    L = ||x - c||^2 + lam * (a . x - b).
    """
    # Your code here
    return list(c), 0.0
