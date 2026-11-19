def determinant(M):
    if not M or any(len(row) != len(M) for row in M):
        raise ValueError("square")
    if len(M) == 1:
        return M[0][0]
    return sum(M[0][j] * determinant([row[:j] + row[j + 1:] for row in M[1:]]) for j in range(len(M)))
