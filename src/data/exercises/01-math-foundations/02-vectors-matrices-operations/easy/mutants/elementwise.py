def matmul(A, B):
    m, n, p = len(A), len(A[0]), len(B[0])
    if len(B) != n:
        raise ValueError("shape")
    return [[A[i][j] * B[i][j] for j in range(p)] for i in range(m)]
