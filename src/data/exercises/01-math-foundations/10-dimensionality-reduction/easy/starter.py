def center(X):
    """Subtract each column's mean from that column; returns new rows."""
    n, d = len(X), len(X[0])
    means = [sum(row[j] for row in X) / n for j in range(d)]
    # TODO: return new rows with means[j] subtracted from column j
    raise NotImplementedError
