def eigenpairs(M):
    """Two (eigenvalue, unit eigenvector) pairs of a real 2x2 matrix, largest eigenvalue first.

    Raises ValueError if the eigenvalues are complex or there aren't two independent eigenvectors.
    """
    (a, b), (c, d) = M
    trace = a + d
    det = a * d - b * c
    disc = trace ** 2 - 4 * det
    if disc < -1e-12:
        raise ValueError("complex eigenvalues: no real eigenvectors")
    if abs(disc) <= 1e-12:
        lam = trace / 2
        if abs(b) <= 1e-12 and abs(c) <= 1e-12:
            return [(lam, [1.0, 0.0]), (lam, [0.0, 1.0])]
        raise ValueError("repeated eigenvalue with a single eigenvector direction")
    root = disc ** 0.5
    pairs = []
    for lam in ((trace + root) / 2, (trace - root) / 2):
        if abs(b) > 1e-12:
            v = [b, lam - a]
        elif abs(c) > 1e-12:
            v = [lam - d, c]
        elif abs(lam - a) <= abs(lam - d):
            v = [1.0, 0.0]
        else:
            v = [0.0, 1.0]
        length = (v[0] ** 2 + v[1] ** 2) ** 0.5
        pairs.append((lam, [v[0] / length, v[1] / length]))
    return pairs
