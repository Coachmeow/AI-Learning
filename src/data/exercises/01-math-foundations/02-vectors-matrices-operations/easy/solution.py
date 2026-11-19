def matmul(A, B):
    """(m x n) @ (n x p) -> m x p, as lists of rows."""
    m, n, p = len(A), len(A[0]), len(B[0])
    if len(B) != n:
        raise ValueError(f"inner dimensions differ: ({m} x {n}) @ ({len(B)} x {p})")
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)] for i in range(m)]
