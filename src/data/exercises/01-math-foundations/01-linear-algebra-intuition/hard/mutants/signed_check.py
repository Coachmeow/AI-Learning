def matrix_rank(rows):
    """Rank of a matrix given as a list of rows, by Gaussian elimination with a 1e-10 tolerance."""
    m = [list(map(float, r)) for r in rows]
    if not m:
        return 0
    rank = 0
    for c in range(len(m[0])):
        pivot = next((p for p in range(rank, len(m)) if m[p][c] > 1e-10), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        for r in range(len(m)):
            if r != rank and abs(m[r][c]) > 1e-10:
                f = m[r][c] / m[rank][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[rank])]
        rank += 1
        if rank == len(m):
            break
    return rank
