def determinant(M):
    if not M or any(len(row) != len(M) for row in M):
        raise ValueError("square")
    out = 1
    for i in range(len(M)):
        out *= M[i][i]
    return out
