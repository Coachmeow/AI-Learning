def matmul(A, B):
    m, n, p = len(A), len(A[0]), len(B[0])
    if len(B) != n:
        raise ValueError("shape")
    return [[sum(A[j][k] * B[k][i] for k in range(n)) for j in range(m)] for i in range(p)]
