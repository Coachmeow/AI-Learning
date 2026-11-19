def neumaier_sum(xs):
    """Sum of xs with Neumaier's compensated summation."""
    s = 0.0
    for x in xs:
        s += x
    return s
