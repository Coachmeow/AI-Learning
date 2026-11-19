import math


def rank_for_error(singular_values, max_rel_error):
    """Smallest k whose rank-k approximation has relative Frobenius error <= max_rel_error."""
    if any(s < 0 for s in singular_values):
        raise ValueError("singular values can't be negative")
    sq = sorted(singular_values, reverse=True)
    total = sum(sq)
    if total == 0:
        return 0
    for k in range(len(sq) + 1):
        if sum(sq[k:]) / total <= max_rel_error:
            return k
    return len(sq)
