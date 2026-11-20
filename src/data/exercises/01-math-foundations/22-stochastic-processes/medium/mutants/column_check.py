def stationary_distribution(P, tol=1e-12, max_iter=100000):
    """Stationary distribution of the row-stochastic matrix P by the power method."""
    n = len(P)
    if n == 0 or any(len(row) != n for row in P):
        raise ValueError("P must be a non-empty square matrix")
    for c in range(n):
        row = [P[r][c] for r in range(n)]
        if any(p < 0 for p in row):
            raise ValueError("probabilities must be non-negative")
        if abs(sum(row) - 1) > 1e-9:
            raise ValueError("every row must sum to 1")
    pi = [1 / n] * n
    for _ in range(max_iter):
        new = [sum(pi[i] * P[i][j] for i in range(n)) for j in range(n)]
        change = sum(abs(a - b) for a, b in zip(new, pi))
        pi = new
        if change < tol:
            return pi
    raise RuntimeError(f"no convergence in {max_iter} iterations")
