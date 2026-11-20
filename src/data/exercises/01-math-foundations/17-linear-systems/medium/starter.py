import math


def cholesky(A):
    """Return the lower triangular L with A = L @ L^T.

    Raise ValueError if A is not symmetric or not positive definite.
    """
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    # Your code here
    return L
