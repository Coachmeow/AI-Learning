def determinant(M):
    if len(M) == 1:
        return M[0][0]
    total = 0
    for j in range(len(M)):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * determinant(minor)
    return total
