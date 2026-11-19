def low_rank(terms, k):
    """Sum of sigma * u * v^T over the first k (sigma, u, v) terms."""
    m, n = len(terms[0][1]), len(terms[0][2])
    out = [[0.0] * n for _ in range(m)]
    for sigma, u, v in terms[:k]:
        for i in range(m):
            for j in range(n):
                out[i][j] += sigma * u[j % m] * v[i % n]
    return out
