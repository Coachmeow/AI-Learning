import math


def conjugate_gradient(A, b, tol=1e-10, max_iter=None):
    """Solve Ax = b for a symmetric positive definite A.

    Return (x, iterations). Raise RuntimeError if it does not converge
    within max_iter iterations (default n), and ValueError if p . Ap <= 0.
    """
    n = len(b)
    if max_iter is None:
        max_iter = n
    x = [0.0] * n
    r = list(b)
    p = list(r)
    rr = sum(v * v for v in r)
    target = tol * math.sqrt(sum(v * v for v in b))
    k = 0
    while math.sqrt(rr) > target:
        if k == max_iter:
            raise RuntimeError(f"no convergence in {max_iter} iterations")
        Ap = [sum(A[i][j] * p[j] for j in range(n)) for i in range(n)]
        pAp = sum(p[i] * Ap[i] for i in range(n))
        if pAp <= 0:
            raise ValueError("A is not positive definite")
        alpha = rr / pAp
        x = [x[i] + alpha * p[i] for i in range(n)]
        r = [r[i] - alpha * Ap[i] for i in range(n)]
        rr_new = sum(v * v for v in r)
        p = list(r)
        rr = rr_new
        k += 1
    return x, k
