def matmul(A, B):
    """(m x n) @ (n x p) -> m x p, as lists of rows."""
    m, n, p = len(A), len(A[0]), len(B[0])
    if len(B) != n:
        raise ValueError(f"inner dimensions differ: ({m} x {n}) @ ({len(B)} x {p})")
    # TODO: cell (i, j) is the dot product of row i of A with column j of B
    raise NotImplementedError
