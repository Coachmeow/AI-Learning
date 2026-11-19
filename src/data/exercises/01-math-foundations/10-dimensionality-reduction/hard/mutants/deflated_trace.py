import math


def pca(X, k):
    """(components, ratios): the top k principal directions by power iteration with deflation."""
    n, d = len(X), len(X[0])
    means = [sum(row[j] for row in X) / n for j in range(d)]
    Z = [[row[j] - means[j] for j in range(d)] for row in X]
    C = [[sum(z[i] * z[j] for z in Z) / (n - 1) for j in range(d)] for i in range(d)]
    total = sum(C[i][i] for i in range(d))

    def matvec(M, v):
        return [sum(M[i][j] * v[j] for j in range(d)) for i in range(d)]

    components, ratios = [], []
    for _ in range(k):
        v = [float(i + 1) for i in range(d)]
        for _ in range(500):
            w = matvec(C, v)
            length = math.sqrt(sum(x * x for x in w))
            v = [x / length for x in w]
        lam = sum(a * b for a, b in zip(v, matvec(C, v)))
        C = [[C[i][j] - lam * v[i] * v[j] for j in range(d)] for i in range(d)]
        first = next(x for x in v if abs(x) > 1e-9)
        if first < 0:
            v = [-x for x in v]
        components.append(v)
        ratios.append(lam / (lam + sum(C[i][i] for i in range(d))))
    return components, ratios
