from itertools import product


def paired_permutation_test(a, b):
    """Exact two-sided p-value for the paired differences b - a, by flipping every sign pattern."""
    if len(a) != len(b) or not a or len(a) > 16:
        raise ValueError("a and b must be the same length, between 1 and 16")
    d = [y - x for x, y in zip(a, b)]
    observed = abs(sum(d))
    count = 0
    for signs in product([1, -1], repeat=len(d)):
        if abs(sum(s * x for s, x in zip(signs, d))) > observed + 1e-12:
            count += 1
    return count / 2 ** len(d)
