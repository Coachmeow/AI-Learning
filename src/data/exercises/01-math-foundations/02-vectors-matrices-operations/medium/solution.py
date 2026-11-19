def determinant(M):
    """Determinant of a square matrix (list of rows) by cofactor expansion along the first row."""
    if not M or any(len(row) != len(M) for row in M):
        raise ValueError("determinant() needs a non-empty square matrix")
    if len(M) == 1:
        return M[0][0]
    total = 0
    for j in range(len(M)):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * determinant(minor)
    return total
