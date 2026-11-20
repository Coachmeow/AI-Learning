import math


def conjugate_gradient(A, b, tol=1e-10, max_iter=None):
    """Solve Ax = b for a symmetric positive definite A.

    Return (x, iterations). Raise RuntimeError if it does not converge
    within max_iter iterations (default n), and ValueError if p . Ap <= 0.
    """
    n = len(b)
    x = [0.0] * n
    # Your code here
    return x, 0
