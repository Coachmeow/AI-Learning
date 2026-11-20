def project_l1(v, radius):
    """Euclidean projection of v onto {w : sum(|w_i|) <= radius}."""
    if radius <= 0:
        raise ValueError("radius must be positive")
    if sum(abs(x) for x in v) <= radius:
        return list(v)
    u = sorted((abs(x) for x in v), reverse=True)
    total = 0.0
    theta = 0.0
    for k, uk in enumerate(u, start=1):
        total += uk
        t = (total - radius) / k
        if uk > t:
            theta = t
    return [(1 if x > 0 else -1) * max(abs(x) - theta, 0.0) for x in v]
