def absorbing_analysis(P):
    """Return (B, t): absorption probabilities and expected steps per transient state."""
    n = len(P)
    if n == 0 or any(len(row) != n for row in P):
        raise ValueError("P must be a non-empty square matrix")
    for row in P:
        if any(p < 0 for p in row) or abs(sum(row) - 1) > 1e-9:
            raise ValueError("every row must be a probability distribution")
    absorbing = [i for i in range(n) if P[i][i] == 1]
    transient = [i for i in range(n) if P[i][i] != 1]
    if not absorbing:
        raise ValueError("there are no absorbing states")
    m, a = len(transient), len(absorbing)
    # Augmented matrix [I - Q | R | 1]
    M = []
    for r, i in enumerate(transient):
        row = [(1.0 if r == c else 0.0) - P[i][j] for c, j in enumerate(transient)]
        row += [P[i][j] for j in absorbing] + [1.0]
        M.append(row)
    for col in range(m):
        piv = max(range(col, m), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            raise ValueError("I - Q is singular: some transient state is never absorbed")
        M[col], M[piv] = M[piv], M[col]
        for r in range(m):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    B = [[M[r][m + k] / M[r][r] for k in range(a)] for r in range(m)]
    t = [M[r][m + a] / M[r][r] for r in range(m)]
    return B, t
