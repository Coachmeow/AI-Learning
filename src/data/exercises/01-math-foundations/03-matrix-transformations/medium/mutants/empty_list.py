def compose(steps):
    """One 2x2 matrix that applies every matrix in steps, the first one first."""
    if not steps:
        return []
    result = [[1.0, 0.0], [0.0, 1.0]]
    for M in steps:
        result = [[sum(M[i][k] * result[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    return result
