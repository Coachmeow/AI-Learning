def covariance_matrix(X):
    """d x d sample covariance (divide by n - 1) of the columns of X."""
    n = len(X)
    if n < 2:
        raise ValueError("need at least 2 samples")
    d = len(X[0])
    means = [sum(row[j] for row in X) / n for j in range(d)]
    Z = [[row[j] - means[j] for j in range(d)] for row in X]
    return [[sum(z[i] * z[j] for z in Z) / (n - 1) for j in range(d)] for i in range(d)]
