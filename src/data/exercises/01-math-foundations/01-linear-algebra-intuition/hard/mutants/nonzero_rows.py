def matrix_rank(rows):
    return sum(1 for r in rows if any(abs(x) > 1e-10 for x in r))
