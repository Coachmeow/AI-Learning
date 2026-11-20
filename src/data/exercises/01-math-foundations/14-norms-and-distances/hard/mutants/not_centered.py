import math


def _covariance(data):
    n, d = len(data), len(data[0])
    means = [sum(row[j] for row in data) / n for j in range(d)]
    Z = [list(row) for row in data]
    return [[sum(z[i] * z[j] for z in Z) / (n - 1) for j in range(d)] for i in range(d)]


def _solve(S, b):
    d = len(b)
    M = [list(S[i]) + [b[i]] for i in range(d)]
    for c in range(d):
        p = max(range(c, d), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-12:
            raise ValueError("the covariance matrix is singular")
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, d):
            f = M[r][c] / M[c][c]
            M[r] = [a - f * b2 for a, b2 in zip(M[r], M[c])]
    z = [0.0] * d
    for i in range(d - 1, -1, -1):
        z[i] = (M[i][d] - sum(M[i][j] * z[j] for j in range(i + 1, d))) / M[i][i]
    return z


def mahalanobis(x, y, data):
    """Mahalanobis distance between x and y under the sample covariance of data."""
    S = _covariance(data)
    diff = [a - b for a, b in zip(x, y)]
    z = _solve(S, diff)
    return math.sqrt(sum(a * b for a, b in zip(diff, z)))
