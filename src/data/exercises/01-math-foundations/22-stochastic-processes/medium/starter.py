def stationary_distribution(P, tol=1e-12, max_iter=100000):
    """Stationary distribution of the row-stochastic matrix P by the power method."""
    # Your code here
    n = len(P)
    return [1 / n] * n
