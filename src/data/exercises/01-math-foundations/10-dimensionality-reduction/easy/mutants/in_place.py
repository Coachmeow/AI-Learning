def center(X):
    """Subtract each column's mean from that column; returns new rows."""
    n, d = len(X), len(X[0])
    means = [sum(row[j] for row in X) / n for j in range(d)]
    for row in X:
        for j in range(d):
            row[j] -= means[j]
    return X
