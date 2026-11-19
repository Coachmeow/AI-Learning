def matmul(A, B):
    m, n, p = len(A), len(A[0]), len(B[0])
    if len(B) != n:
        raise ValueError("shape")
    return [[sum(A[i][k] * B[j][k] for k in range(n)) for j in range(p)] for i in range(m)]
