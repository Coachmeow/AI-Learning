def neumaier_sum(xs):
    """Sum of xs with Neumaier's compensated summation."""
    s = 0.0
    c = 0.0
    for x in xs:
        t = s + x
        c += (s - t) + x
        s = t
    return s + c
