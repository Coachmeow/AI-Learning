def back_substitution(U, b):
    """Solve Ux = b for an upper triangular U, from the last row up."""
    n = len(b)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = 0.0  # TODO: use b[i], s and the diagonal entry U[i][i]
    return x
