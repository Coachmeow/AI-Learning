def compose(steps):
    """One 2x2 matrix that applies every matrix in steps, the first one first."""
    result = [[1.0, 0.0], [0.0, 1.0]]
    for M in steps:
        result = [[M[i][j] * result[i][j] for j in range(2)] for i in range(2)]
    return result
