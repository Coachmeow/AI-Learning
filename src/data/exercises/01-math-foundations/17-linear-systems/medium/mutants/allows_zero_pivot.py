import math


def cholesky(A):
    """Return the lower triangular L with A = L @ L^T.

    Raise ValueError if A is not symmetric or not positive definite.
    """
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("A must be square")
    for i in range(n):
        for j in range(i):
            if abs(A[i][j] - A[j][i]) > 1e-9:
                raise ValueError("A is not symmetric")
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s < 0:
                    raise ValueError("A is not positive definite")
                L[i][j] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L
