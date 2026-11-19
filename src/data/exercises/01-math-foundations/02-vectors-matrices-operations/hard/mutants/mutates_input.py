def inverse(A):
    """Inverse of a square matrix by Gauss-Jordan with partial pivoting; ValueError if singular."""
    n = len(A)
    if n == 0 or any(len(row) != n for row in A):
        raise ValueError("inverse() needs a non-empty square matrix")
    aug = A
    for i, row in enumerate(aug):
        row.extend(1.0 if i == j else 0.0 for j in range(n))
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(aug[r][c]))
        if abs(aug[p][c]) < 1e-12:
            raise ValueError("matrix is singular")
        aug[c], aug[p] = aug[p], aug[c]
        pivot = aug[c][c]
        aug[c] = [x / pivot for x in aug[c]]
        for r in range(n):
            if r != c:
                f = aug[r][c]
                if f:
                    aug[r] = [x - f * y for x, y in zip(aug[r], aug[c])]
    return [row[n:] for row in aug]
